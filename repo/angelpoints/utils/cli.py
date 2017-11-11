'''
Created on Sep 13, 2016

@author: ross.hodapp
'''
from abc import ABC, abstractmethod
import argparse

class CLIBase(ABC):
    """ Useful mixin for simple command line scripts, where you subclass this and specify a 'arguments' class attribute.
        Forces a run() method to be defined in the subclass, which is called right after instantiation.
    """
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.__class__.__doc__)  # Should get the subclass' docstring
        for a in self.arguments:
            self.parser.add_argument(a[0], **a[1])
        self.run(self.parser.parse_args())
    
    @abstractmethod
    def run(self, args):
        raise NotImplementedError('Define a run() method')
