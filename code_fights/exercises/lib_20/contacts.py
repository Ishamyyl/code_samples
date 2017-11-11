from collections import namedtuple, UserList

class Contacts(UserList):
    def __init__(self):
        UserList.__init__(self)
        self.factory = namedtuple('Contacts', 'name, lives_in, email')

    def add(self, name, info):
        self.append(self.factory(name, **info))

    def contacts_by_lives_in(self, lives_in):
        return [c.name for c in self.data if c.lives_in == lives_in]
