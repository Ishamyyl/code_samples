'''
Created on Sep 13, 2016

@author: ross.hodapp
'''
from collections import ChainMap
from contextlib import contextmanager

from angelpoints.utils.constants import hostname, db_pass, db_user
from mysql.connector import connect


class DatabaseConnection:
    """ Establishes a DB connection on initialization into self.connection. 
        When subclassing, set the following class attributes. When creating directly, pass the following to the constructor.
            user, passwd, host, port, database
    """
    
    # defaults
    if 'dv' in hostname:
        host = 'redacted'
    elif 'qa' in hostname:
        host = 'redacted'
    elif 'test' in hostname:
        host = 'redacted'
    elif hostname == 'redacted':
        host = 'redacted'
    else:
        raise ValueError('Unknown host. For local dev, modify this module')
    connection_defaults = dict(
        host=host,
        port='redacted',
        database='redacted',
        user=db_user,
        passwd=db_pass,
    )
    
    cursor_args = {'dictionary': True, 'buffered': True}
    
    def __init__(self, **kwargs):
        self.connection_args = ChainMap(kwargs, self.connection_defaults)  # Fast way for given args to preside before defaults
        self.reconnect()
    
    @contextmanager
    def getCursorWithClose(self, **kwargs):
        """ Utility method to open a new cursor and guarantee it's closed.
            Pass cursor keyword arguments. If not, the cursor args from the class constructor will be used.
        """
        c_a = kwargs or self.cursor_args
        csr = self.connection.cursor(**c_a)
        yield csr
        csr.close()
        
    def reconnect(self):
        """ Really only needed if you change self.connection_args, such as when switching databases. 
        """
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
        self.connection = connect(**self.connection_args)
    
    def send(self, sql, **kwargs):
        """ For UPDATEs, INSERTs, DELETEs. No affected-rows results returned currently
        """
        with self.getCursorWithClose(**kwargs) as csr:
            csr.execute(sql)
        
    def get(self, sql, **kwargs):
        """ Returns results of a SQL call, as a list of dictionaries by (our) default.
        """
        with self.getCursorWithClose(**kwargs) as csr:
            csr.execute(sql)
            return csr.fetchall()
        
    def getOneRow(self, sql, **kwargs):
        """ Returns the first result of a SQL call, as a dictionary by (our) default. Whole query is executed, just first result fetched over the network.
        """
        with self.getCursorWithClose(**kwargs) as csr:
            csr.execute(sql)
            return csr.fetchone()
    
    def getOneColumn(self, sql, **kwargs):
        """ Helper to return the value of a 1-column select call
        """
        return self.getOneRow(sql, dictionary=False)[0]

if __name__ == '__main__':
    DatabaseConnection()
