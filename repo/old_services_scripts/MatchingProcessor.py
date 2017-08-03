#!/usr/bin/env python
'''
Pulls the Matching Items from the database and formats them in an appropriate manner for Vendor
'''
from _io import StringIO
from ast import literal_eval
from base64 import standard_b64decode, standard_b64encode
from configparser import ConfigParser
from contextlib import closing
import csv
from datetime import date
from pathlib import Path
from platform import node
import re
from subprocess import call
from urllib.parse import urlparse

from mysql.connector import connect
import requests

import gnupg
from simple_salesforce import Salesforce


class MatchingProcessor():
    
    """This Processor is an ugly solution to several key requirements:
        1. A physical file from the disk must be encrypted and sent via FTP to Vendor, currently
            - Couldn't figure out a way to programatically connect to FTP and send an in-memory file-like object
        2. Vendors processing of the file may take an arbitrary number of days for a result
            - Can't leave a call-back thread waiting for a response from Vendor
            - State must be saved while waiting for Vendor, picking up where it left off
            - Required custom arbitrary serialization format via ConfigParser INI-style format
        3. For reference/backup, we must keep the files that were sent to Vendor
            - The files will be on Salesforce anyway, so lets make use of that 
        (4. Nice-to-have) Logging, refernce, and backup comes from 1 source: a Salesforce Task
        (5.) Intended as a single-file script, to be passed around to coworkers and easily used as long as they have Python 3
        
        This was a I-need-to-get-stuff-done, don't-have-time-to-do-it-right script
        
    Improvement suggestions:
        - MatchingProcessor is converted into a generic base class that will work on local files. 
            It is then subclassed to TaskMatchingProcessor that handles all the file I/O and state. 
        
        - Update the executeNextStep() mechanic. What a hack. 
        
        - Turn this into a subclass of Report too
    """
    
    base_dir = r"redacted"  # if the directory path has backslashes '\' be sure to use the r prefix, i.e. r'foo\bar'
    gpg_dir = r"redacted/.gnupg"
    
    # Salesforce and Angelpoints Database connection credentials
    sf_hash = 'redacted'
    db_hash = "redacted"
    
    
    sf_auth = dict(zip(['username', 'password', 'security_token'], sf_hash))
    isTunnelled = 'redacted' not in node()
    db_auth = {'user': db_hash[0], 'passwd': db_hash[1], 'host': '127.0.0.1' if isTunnelled else 'redacted', 'port': 'redacted' if isTunnelled else 'redacted', 'database': ''}
    sf_rest_attachment_by_id = 'https://na11.salesforce.com/services/data/v29.0/sobjects/Attachment/{id}/Body'
    
    me_preferred_time_format = '%Y%m%d'  # YYYYMMDD
    file_name_format = '{name}_{date}_{t}{vif}.txt'
    version_identifier_format = '_v{v}'
    config_note_format = 'Config'
    matches_note_format = 'Matches_v{v}.txt'
    deferred_note_format = 'Deferred.txt'
    invalid_note_format = 'Invalid.txt'
    invalid_file_cleared_format = '- rhodapp Cleared'
    comment_format = 'Auto-comment from MatchingProcessor.py'
    
    batch_header_format = ["Batch", "PartnerSource", "PartnerCampaign", "PartnerBatchIdentifier", "DonorDetailsLevel", "TotalAmount", "PartnerBatchComments"]
    donation_header_format = ["Donation", "DonorFirstName", "DonorLastName", "DonorEmail", "DonorAddress1", "DonorAddress2", "DonorCity", "DonorState", "DonorZip", "DonorCountry", "DonorPhone", "DonorToken", "PartnerTransactionIdentifier", "TipAmount"]
    donation_line_item_format = ["DonationLineItem", "NPOEIN", "ItemAmount", "Dedication", "Designation", "DonorVisibility", "AddOrDeduct", "TransactionType", "IsMatchingDonation", "MatchType", "OriginalDonationAmount", "OriginalDonationDate", "MatchFor", "OriginalDonationPartnerTransactionID", "OriginalDonationReference", "Notes"]
    
    backwards_clients = ['redacted', 'redacted', 'redacted']
    
    def __init__(self, task=None):
        print('^ initializing')
        self.sf = Salesforce(sandbox=False, **self.sf_auth)
        self.base_dir = Path(self.base_dir)
        self.gpg_dir = Path(self.gpg_dir)
        if not self.base_dir.is_dir(): 
            raise
        self.__getID(task)
        self.config = ConfigParser()
        self.__loadIni()
        print('v initialized')
        
    def __loadIni(self):
        print('^ loading config')
        self.notes = {n['Title']: n['attributes']['url'].split('/')[-1] for n in self.sf.query(self.soql['select']['notes_list'].format(id=self.id))['records']}  # get a mapping of {Note: 'Url to note'} from the task
        
        # Do we have a config Note already created?
        if self.config_note_format not in self.notes:
            self.__createIni()
            self.config.read_string(self.sf.Note.get(self.config['notes']['config'])['Body'])
        else:
            self.config.read_string(self.sf.Note.get(self.notes[self.config_note_format])['Body'])
        print('v config loaded')
        
    def __createIni(self):
        print('^ creating config')
        self.config.read_string(self.matching_ini_shell)
        self.db_auth['database'] = 'central'
        with closing(connect(**self.db_auth)) as cnx:
            with closing(cnx.cursor(dictionary=True, buffered=True)) as csr: 
                csr.execute(self.sql['select']['central.clients.database_name-via-url'].format(url=self.client_url))
                __r = csr.fetchall()[0]  # assuming only 1 result
        self.config['client']['client'] = __r['full_name']
        self.config['client']['database'] = __r['database_name']
        self.config['info']['date'] = date.today().strftime(self.me_preferred_time_format)
        
        # initialize the config Note and several attachments needed
        self.config['notes']['config'] = self.sf.Note.create({'ParentId': self.id, 'IsPrivate': True, 'Title': self.config_note_format, 'Body': ''})['id']
        self.config['files']['deferred'] = self.sf.Attachment.create({'ParentId': self.id, 'IsPrivate': False, 'Name': self.deferred_note_format, 'ContentType': 'text/plain', 'Body': ''})['id'][:-3]
        self.config['files']['invalid'] = self.sf.Attachment.create({'ParentId': self.id, 'IsPrivate': False, 'Name': self.invalid_note_format, 'ContentType': 'text/plain', 'Body': ''})['id'][:-3]
        
        _batchName = self.sf.TASKRAY__Project_Task__c.get(self.id)['TFS_Issue__c']
        print(_batchName)
        if input('Using "{batch}" - Continue? >'.format(batch=_batchName)).startswith('y'):
            self.db_auth['database'] = self.config['client']['database']
            with closing(connect(**self.db_auth)) as cnx:
                with closing(cnx.cursor(dictionary=True, buffered=True)) as csr: 
                    csr.execute("""redacted;""".format(batch=_batchName, client=self.config['client']['database']))
                    __r = csr.fetchall()[0]  # assuming only 1 result
            print('Using Batch ID', __r['batch_id'])
            self.config['info']['batch'] = str(__r['batch_id'])
        else:
            print('Stopping execution')
            exit(0)
        
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        self.sf.TaskRay_Task_Comments__c.create({'TaskRay_Task__c': self.id, 'Name': 'Initialized', 'Comments__c': 'Auto-comment from MatchingProcessor.py'})
        print('v config created')
    
    def __getID(self, task):
        print('^ getting Salesforce info')
        if task:
            if task.startswith('PROF'):
                __select_urlFromTask = self.soql['select']['select_url_from_task'].format(obj='Task_ID__c', value=task)
            elif task.startswith('http'):
                __select_urlFromTask = self.soql['select']['select_url_from_task'].format(obj='Id', value=urlparse(task).path.strip('/'))
            else:
                raise
        else:
            raise
        __sf_result = self.sf.query(__select_urlFromTask)
        self.id = __sf_result['records'][0]['attributes']['url'].split('/')[-1]
        self.client_url = urlparse(__sf_result['records'][0]['Account__r']['AP_Production_URL__c']).netloc
        print(__sf_result['records'][0]['Account__r']['AP_Production_URL__c'])
        print('v id retrieved: ', self.client_url)
        
    def _recalculateTotalAmount(self):
        print('^ recalculating')
        self.total_amount = 0
        for item in self.matches:
            self.total_amount += float(item['ItemAmount'])
        self.batch_header["TotalAmount"] = "{0:.2f}".format(self.total_amount)
        print('v totals recalculated')
        
    def _writeFiles(self):
        print('^ writing files to SF')
        if self.matches:
            with StringIO() as f_matches:
                __writer = csv.DictWriter(f_matches, delimiter='\t', fieldnames=self.batch_header_format)
                __writer.writerow(self.batch_header)
                __writer.fieldnames = self.donation_header_format
                __writer.writerow(self.donation_header)
                __writer.fieldnames = self.donation_line_item_format
                for match in self.matches:
                    if match['Designation']:
                        match['Designation'] = match['Designation'].replace('\r', '').replace('\n', '')
                    if match['Dedication']:
                        match['Dedication'] = match['Dedication'].replace('\r', '').replace('\n', '')
                    __writer.writerow(match)
                self.config['files']['matches'] = self.sf.Attachment.create({'ParentId': self.id, 'IsPrivate': False, 'Name': self.matches_note_format.format(v=self.config['progress']['version']), 'ContentType': 'text/plain', 'Body': repr(standard_b64encode(bytes(f_matches.getvalue(), 'utf8')))[2:-1]})['id'][:-3]
        if self.deferred:
            with StringIO() as f_deferred:
                __writer = csv.DictWriter(f_deferred, delimiter='\t', fieldnames=self.donation_line_item_format)
                for match in self.deferred:
                    if match['Designation']:
                        match['Designation'] = match['Designation'].replace('\r', '').replace('\n', '')
                    if match['Dedication']:
                        match['Dedication'] = match['Dedication'].replace('\r', '').replace('\n', '')
                    __writer.writerow(match)
                self.sf.Attachment.delete(self.config['files']['deferred'])
                self.config['files']['deferred'] = self.sf.Attachment.create({'ParentId': self.id, 'IsPrivate': False, 'Name': self.deferred_note_format, 'ContentType': 'text/plain', 'Body': repr(standard_b64encode(bytes(f_deferred.getvalue(), 'utf8')))[2:-1]})['id'][:-3]
        if self.invalid:
            with StringIO() as f_invalid:
                __writer = csv.DictWriter(f_invalid, delimiter='\t', fieldnames=self.donation_line_item_format)
                for match in self.invalid:
                    if match['Designation']:
                        match['Designation'] = match['Designation'].replace('\r', '').replace('\n', '')
                    if match['Dedication']:
                        match['Dedication'] = match['Dedication'].replace('\r', '').replace('\n', '')
                    __writer.writerow(match)
                self.sf.Attachment.delete(self.config['files']['invalid'])
                self.config['files']['invalid'] = self.sf.Attachment.create({'ParentId': self.id, 'IsPrivate': False, 'Name': self.invalid_note_format, 'ContentType': 'text/plain', 'Body': repr(standard_b64encode(bytes(f_invalid.getvalue(), 'utf8')))[2:-1]})['id'][:-3]
        print('v files written')
        
    def _readFiles(self):
        print('^ loading files')
        __body = requests.get(self.sf_rest_attachment_by_id.format(id=self.config['files']['matches']), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.sf.session_id)}).text
        if __body:
            with StringIO(__body) as f_matches:
                __reader = csv.DictReader(f_matches, delimiter='\t', fieldnames=self.batch_header_format)
                self.batch_header = next(__reader)
                __reader.fieldnames = self.donation_header_format
                self.donation_header = next(__reader)
                __reader.fieldnames = self.donation_line_item_format
                self.matches = list(__reader)
        else:
            self.matches = []
        __body = requests.get(self.sf_rest_attachment_by_id.format(id=self.config['files']['deferred']), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.sf.session_id)}).text
        if __body:
            with StringIO(__body) as f_deferred:
                __reader = csv.DictReader(f_deferred, delimiter='\t', fieldnames=self.donation_line_item_format)
                self.deferred = list(__reader)
        else:
            self.deferred = []
        __body = requests.get(self.sf_rest_attachment_by_id.format(id=self.config['files']['invalid']), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.sf.session_id)}).text
        if __body:
            with StringIO(__body) as f_invalid:
                __reader = csv.DictReader(f_invalid, delimiter='\t', fieldnames=self.donation_line_item_format)
                self.invalid = list(__reader)
        else:
            self.invalid = []
        print('v files loaded')
            
    def step_reconcile(self):
        print('^ reconciling')
        __approved_status = self.enums['redacted.status']['APPROVED']
        with closing(self.db.cursor(dictionary=True, buffered=True)) as csr:
            if self.matches:
                __um = self.sql['update']['reconciliation'].format(date='NOW()', status=__approved_status, list=','.join(["'{}'".format(m['OriginalDonationReference']) for m in self.matches]))
                print('Evaluate this SQL for matching reconciliation: ')
                print(__um)
                if not input('Continue? >').startswith('y'):
                    print('Stopping execution')
                    exit(0)
                csr.execute(__um)
            else: 
                print("- no matches to reconcile, probable error")
            if self.deferred:
                __ud = self.sql['update']['reconciliation'].format(date='NULL', status=self.enums['redacted.status']['DEFERRED'], list=','.join(["'{}'".format(m['OriginalDonationReference']) for m in self.deferred]))
                print('Evaluate this SQL for deferred reconciliation: ')
                print(__ud)
                if not input('\nContinue? >').startswith('y'):
                    print('Stopping execution')
                    exit(0)
                csr.execute(__ud)
            else: 
                print("- no deferred to reconcile")
            if self.invalid:
                __ui1 = self.sql['update']['reconciliation'].format(date='NULL', status=self.enums['redacted.status']['INVALID_NPO'], list=', '.join(["'{}'".format(m['OriginalDonationReference']) for m in self.invalid]))
                __ui2 = self.sql['update']['remove_from_batch'].format(list=', '.join(["'{}'".format(m['OriginalDonationReference']) for m in self.invalid]))
                print('Evaluate this SQL for invalid reconciliation: ')
                print(__ui1)
                if not input('Continue? >').startswith('y'):
                    print('Stopping execution')
                    exit(0)
                csr.execute(__ui1)
                csr.execute(__ui2)
            else: 
                print("- no invalid to reconcile")
            self.db.commit()
            print("\n- Check the frontend for the Record Count, Donor Count, and Total Amount calculations\n")
            csr.execute(self.sql['update']['static_calcs'].format(ds=input("Record Count? >"), uds=input("Donor Count? >"), tdv=input("Total Amount? >"), batch=self.config['info']['batch']))
            csr.execute(self.sql['update']['batch_status'].format(status=self.enums['redacted.status']['Complete'], batch=self.config['info']['batch']))
            self.db.commit()
        self.sf.Note.update(self.config['notes']['nextResponse'], {'Body': 'Vendor Accepted this version'})
        self.config['notes']['nextResponse'] = ''
        self.sf.TaskRay_Task_Comments__c.create({'TaskRay_Task__c': self.id, 'Name': 'Reconciled', 'Comments__c': 'Auto-comment from MatchingProcessor.py'})
        self.sf.TASKRAY__Project_Task__c.update(self.id, {'TASKRAY__List__c': 'Finished', 'Log_Time_hrs__c': '0.25', 'QA_Notes__c': ' - {}- Completed automatically with MatchingProcessor.py by Ross Hodapp'.format(date.today().strftime('%m/%d'))})
        self.config['progress']['state'] = 'fin'
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        print('v reconciled')
    
    def step_handleErrors(self):
        __response = self.sf.Note.get(self.config['notes']['nextResponse'])['Body'].split('\r\n')
        if __response[-1] != self.invalid_file_cleared_format:
            __bad_eins = set(m.group(1) for m in map(self.regex['ein'].search, __response) if m)
            if __bad_eins:
                print('^ handling bad EINs')
                for i in self.matches.copy():
                    if i['NPOEIN'] in __bad_eins:
                        self.invalid.append(i)
                        self.matches.remove(i)
                    if not i['NPOEIN']:
                        self.invalid.append(i)
                        self.matches.remove(i)
            else:
                print('errors with file format')
                self.config['progress']['state'] = 'backFromVendor'
                with StringIO() as f_config:
                    self.config.write(f_config)
                    self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
                raise  # invalid file
        self.config['progress']['version'] = str(self.config['progress'].getint('version') + 1)
        self.config['progress']['state'] = 'aggregate'
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        print('v errors handled')
        self.executeNextStep()
            
    def step_backFromVendor(self):  # "entry point"
        print('^ back from Vendor')
        self._readFiles()
        if literal_eval(str(self.sf.TASKRAY__Project_Task__c.get(self.id)['Vendor_Accepted__c'])):  # Getting a malformed error? it returned something not in (str('True'), str('False'))
            self.config['progress']['state'] = 'reconcile'
        else:
            self.config['progress']['state'] = 'handleErrors'
        self.sf.TaskRay_Task_Comments__c.create({'TaskRay_Task__c': self.id, 'Name': 'v{v} back from Vendor'.format(v=self.config['progress']['version']), 'Comments__c': self.comment_format})
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        self.executeNextStep()
            
    def step_sendToVendor(self):
        print('^ sending to Vendor')
        call(['filezilla', '-c0/Vendor', '-a{}'.format((self.base_dir / 'pgp').as_posix())])
        self.sf.TASKRAY__Project_Task__c.update(self.id, {'TASKRAY__List__c': 'Pending Verification'})
        self.sf.TaskRay_Task_Comments__c.create({'TaskRay_Task__c': self.id, 'Name': 'Sent v{v} to Vendor'.format(v=self.config['progress']['version']), 'Comments__c': self.comment_format})
        self.config['notes']['nextResponse'] = self.sf.Note.create({'ParentId': self.id, 'Title': 'Vendor response for v{v}'.format(v=self.config['progress']['version']), 'Body': ''})['id']
        for i in (self.base_dir / 'pgp').glob('*.pgp'):
            i.unlink()
        self.config['progress']['state'] = 'backFromVendor'
        with closing(self.db.cursor(dictionary=True, buffered=True)) as csr:
            csr.execute(self.sql['update']['batch_status'].format(status=self.enums['redacted.status']['Processing'], batch=self.config['info']['batch']))
            csr.execute(self.sql['update']['batch_processed_date'].format(batch=self.config['info']['batch']))
            self.db.commit()
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        print('v file sent')
            
    def step_encrypt(self):
        print('^ encrypting')
        __f_matches_name = self.file_name_format.format(name=self.config['client']['database'], date=self.config['info']['date'], t=self.config['info']['type'], vif=self.version_identifier_format.format(v=self.config['progress']['version']))
        with Path(self.base_dir / __f_matches_name).open('w', encoding='utf_8', newline='\n') as f_matches:
            f_matches.write(requests.get(self.sf_rest_attachment_by_id.format(id=self.config['files']['matches']), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.sf.session_id)}).text[:-2])
        gpg = gnupg.GPG(gnupghome=self.gpg_dir.as_posix())
        with Path(self.base_dir / __f_matches_name).open(mode='rb') as f_matches:
            Path(self.base_dir / 'pgp' / (__f_matches_name + '.pgp')).open(mode='w').write(str(gpg.encrypt_file(f_matches, gpg.list_keys()[0]['fingerprint'])))
        self.sf.TASKRAY__Project_Task__c.update(self.id, {'TFS_Issue__c': __f_matches_name})
        self.config['progress']['state'] = 'sendToVendor'
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        print('v file encrypted')
        self.executeNextStep()
        
    def step_aggregate(self):
        print('^ aggregating')
        for i in self.matches.copy():
            if float(i['ItemAmount']) < 10.0:
                self.deferred.append(i)
                self.matches.remove(i)
            if not i['NPOEIN']:
                self.invalid.append(i)
                self.matches.remove(i)
#                 print( "Deferred something: EIN: ", i['NPOEIN'], ' Amount: ', i['ItemAmount'], ' ID: ', i['OriginalDonationReference'], ' len(def): ', len(self.deferred), ' len(matches): ', len( self.matches))
        if self.deferred:
            __eins = {}
            for item in self.deferred:
                __eins[item['NPOEIN']] = float(__eins.setdefault(item['NPOEIN'], 0)) + float(item["ItemAmount"])
            __eins = [k for k, v in __eins.items() if float(v) >= 10.0]
            for i in self.deferred.copy():
                if i['NPOEIN'] in __eins:
                    self.matches.append(i)
                    self.deferred.remove(i)
        
        print('v aggregated')
        print("# Total Matches: ", len(self.matches))
        print("# Total Deferred: ", len(self.deferred))
        print("# Total Invalid: ", len(self.invalid))
        self._recalculateTotalAmount()
        self._writeFiles()
        self.config['progress']['state'] = 'encrypt'
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        self.executeNextStep()
        
    def step_pull(self):
        print('^ pulling')
        with closing(self.db.cursor(dictionary=True, buffered=True)) as csr:
            csr.execute(self.sql['select']['donation_line_item'].format(batch=self.config['info']['batch']))
            self.matches = csr.fetchall()
            self.deferred = []
            self.invalid = []
        with closing(self.db.cursor(dictionary=True, buffered=True)) as csr:
            csr.execute(self.sql['select']['batch_header'].format(batch=self.config['info']['batch']))
            self.batch_header = csr.fetchall()[0]
        with closing(self.db.cursor(dictionary=True, buffered=True)) as csr:
            csr.execute(self.sql['select']['donation_header'])
            self.donation_header = csr.fetchall()[0]
        self.sf.TaskRay_Task_Comments__c.create({'TaskRay_Task__c': self.id, 'Name': 'Pulled v1', 'Comments__c': 'Auto-comment from MatchingProcessor.py'})
        self.config['progress']['state'] = 'aggregate'
        with StringIO() as f_config:
            self.config.write(f_config)
            self.sf.Note.update(self.config['notes']['config'], {'Body': f_config.getvalue()})
        print('v pulled')
        self.executeNextStep()
        
    def executeNextStep(self):
        getattr(self, 'step_{}'.format(self.config['progress']['state']))()

    def run(self):
        self.db_auth['database'] = self.config['client']['database']
        self.db = connect(**self.db_auth)
        self.executeNextStep()
        self.db.close()
    
    sql = {}
    sql['select'] = {
        'central.clients.database_name-via-url': """redacted;""",
        'batch_header': """redacted;""",
        'donation_header': """redacted;""",
        'donation_line_item': """redacted;""",
        'old_donation_line_item': """redacted;"""
    }
    sql['update'] = {
        'reconciliation': """redacted;""",
        'remove_from_batch': """redacted;""",
        'batch_status': """redacted;""",
        'batch_processed_date': """redacted;""",
        'static_calcs': """redacted;"""
}
    soql = {}
    soql['select'] = {
        'notes_list': """SELECT Title FROM Note WHERE ParentId = '{id}'""",
        'select_url_from_task': """SELECT Account__r.AP_Production_URL__c FROM TASKRAY__Project_Task__c WHERE {obj} = '{value}'"""
}
    regex = {}
    regex = {
        'ein': re.compile(r'"(?P<ein>\d{9})"')
}
    
    matching_ini_shell = """
        [info]
            date = 
            type = matching
            batch = 
            
        [files]
            matches =  
            deferred = 
            invalid = 
        
        [notes] 
            config = 
            nextResponse = 
        
        [client]
            database = 
            client = 
        
        [progress]
            state = pull
            version = 1
    """
    enums = {}
    enums['redacted.status'] = ['PROCESSING', 'FAILED', 'COMPLETE', 'DEFERRED', 'INVALID_NPO', 'OBSOLETE_NPO', 'PENDING', 'APPROVED', 'DENIED', 'CANCELLED']
    enums['redacted.status'] = ['__unknown', 'Pending', 'Locked', 'Processing', 'Approved', 'Complete']
    for k, v in enums.items():
        enums[k] = dict(zip(enums[k], range(len(k))))

if __name__ == "__main__":
#     from argparse import ArgumentParser, SUPPRESS
#     parser = ArgumentParser(description="Runs through the entire Matching Gifts process.", argument_default=SUPPRESS)
#     parser.add_argument('task', help="The URL or Task ID of the TaskRay Task that started this process.", default=input("task url? >"))
#     MatchingProcessor(**vars(parser.parse_args())).run()
    MatchingProcessor(task=input("task url? >")).run()

__author__ = 'Ross Hodapp'
__email__ = 'rhodapp@microedge.com'
__updated__ = '20150721'
__version__ = '0.1'
