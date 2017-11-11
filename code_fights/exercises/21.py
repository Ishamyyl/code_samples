#!/usr/bin/env python3

""" Write the class AddressBook so the following code works:
        c = AddressBook()

        c.add(name='ynon', email='ynon@ynonperek.com', likes='red')
        c.add(name='bob', email='bob@gmail.com', likes='blue')
        c.add(name='ynon', email='ynon@gmail.com', likes='blue')

        c.find_by(name='ynon')
        # returns:
        # [
        #   {'name': 'ynon', 'email': 'ynon@ynonperek.com', 'likes': 'red'},
        #   {'name': 'ynon', 'email': 'ynon@gmail.com', 'likes': 'blue}
        # ]

        c.find_by(likes='blue)
        # returns:
        # [
        #   { 'name': 'bob', 'email': 'bob@gmail.com', 'likes': 'blue' },
        #   {'name': 'ynon', 'email': 'ynon@gmail.com', 'likes': 'blue}
        # ]
        
    Code should be generic enough so if new fields are added everything still works.
"""


from collections import UserDict, UserList


class AddressBook(UserList):
    
    def add(self, **kwargs):
        self.data.append(dict(kwargs))
    
    def find_by(self, **kwargs):
        return [i for i in self.data if all(i.get(k) == v for k, v in kwargs.items())]

def run():
    c = AddressBook()
    c.add(name='ynon', email='ynon@ynonperek.com', likes='red', asdf='asdf')
    c.add(name='bob', email='bob@gmail.com', likes='blue')
    c.add(name='ynon', email='ynon@gmail.com', likes='blue')
    print(c.find_by(asdf='ynon'))
    print(c.find_by(likes='blue'))

if __name__ == '__main__':
    run()
