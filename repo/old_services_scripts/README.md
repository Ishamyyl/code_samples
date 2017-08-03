Forgive me for what you are about to see...

This Processor is an ugly solution to several key requirements:
        1. A physical file from the disk must be encrypted and sent via FTP to Vendor, currently
            - Couldn't figure out a way to programatically connect to FTP and send an in-memory file-like object
            - Attempts to do this didn't work
        2. Vendor's processing of the file may take an arbitrary number of days for a result
            - Can't leave a call-back thread waiting for a response from Vendor
            - State must be saved while waiting for Vendor, picking up where it left off
            - Required custom arbitrary serialization format via ConfigParser INI-style format
        3. For reference/backup, we must keep the files that were sent to Vendor
            - The files will be on Salesforce anyway, so lets make use of that 
        (4. Nice-to-have) Logging, refernce, and backup comes from 1 source: a Salesforce Task
        (5.) Intended as a single-file script, to be passed around to coworkers and easily used as long as they have Python 3
        
        This was a I-need-to-get-stuff-done, don't-have-time-to-do-it-right script