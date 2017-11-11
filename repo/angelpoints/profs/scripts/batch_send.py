#!/usr/bin/env python3
'''
Created on Sep 13, 2016

@author: ross.hodapp
'''
import argparse

from angelpoints.utils.cli import CLIBase
from angelpoints.profs.tools.giving import BatchExport

class BatchExportScript(CLIBase):
    
    batch_type_choices = ['d4d', 'vendor', 'ch']
    
    # Overrides default CLI-Base initialization in order to add a pair of required argument groups
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Manually processes and sends various types of batches from Angelpoints")
        subparsers = self.parser.add_subparsers(dest='type')
        subparsers.required = True
        vendor_sub = subparsers.add_parser('vendor')
        d4d_sub = subparsers.add_parser('d4d')
        ch_sub = subparsers.add_parser('ch')
        
        for sub in [d4d_sub, ch_sub, vendor_sub]:
            client_group = sub.add_mutually_exclusive_group(required=True)
            client_group.add_argument('--client-db', help="The database name of the client", type=str)
            client_group.add_argument('--client-id', help="The Account ID of the client", type=int)
            batch_group = sub.add_mutually_exclusive_group(required=True)
            batch_group.add_argument('--batch-name', help="The name of the batch", type=str)
            batch_group.add_argument('--batch-id', help="The ID of the batch from the database", type=int)
            
        self.run(self.parser.parse_args())
    
    def run(self, args):
        BatchExport(**vars(args))
    
if __name__ == '__main__':
    BatchExportScript()
