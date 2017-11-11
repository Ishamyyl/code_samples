#!/usr/bin/env python3

""" 17) Write a class named AddressBook that saves names and email addresses in a file. 

    The following code should work (and create the file if not already exists):
        with AddressBook('contacts.txt') as ab:
            ab.add('Eve', 'eve@gmail.com')
            ab.add('Alice', 'alice@walla.co.il')

        with AddressBook('contacts.txt') as ab:
            print(ab.email('Eve'))
            
    
    18) Modify the class so the following will also work (Hint: read about __getitem__):
        with AddressBook('contacts.txt') as ab:
            print(ab['Eve'])
"""


from collections import UserDict, defaultdict
import csv
from pathlib import Path


class AddressBook(UserDict):

    def __init__(self, file):
        UserDict.__init__(self)
        self.data = defaultdict(str)
        self.file = Path(file)
        if not self.file.exists():
            self.file.touch()
        
    def __enter__(self):
        with self.file.open('r') as f:
            self.data.update(csv.reader(f))
        return self
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.file.open('w') as f:
            writer = csv.writer(f)
            writer.writerows(self.data.items())
        
    def add(self, name, email):
        self.data[name] = email
        
    def email(self, name):
        return self.data[name]

def run():
    with AddressBook('contacts.txt') as ab:
        ab.add('Eve', 'eve@gmail.com')
        ab.add('Alice', 'alice@walla.co.il')
    
    with AddressBook('contacts.txt') as ab:
        print(ab.email('Eve'))
        
    with AddressBook('contacts.txt') as ab:
        print(ab['Eve'])

if __name__ == '__main__':
    run()
