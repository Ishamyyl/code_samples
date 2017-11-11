'''
Created on Sep 20, 2016

@author: Ross.Hodapp
'''
from functools import wraps
import pickle
from types import SimpleNamespace
from angelpoints.utils.constants import pickle_folder


class PersistState:
    """ Helper class to consistently save and load states between script sessions.
        States are saved in the picklejar folder of the cwd (usually the folder of the script definition aka ".../angelpoints/profs/scripts").
    
        Put data in self.state.
        Set a class attribute called state_ids in the following format, where the ids are attributes on self:
            (<prefix>, (<list>, <of>, <unique>, <ids for file>))
        Example:
            ('test', ('client', 'batch'))
        which results in:
            'test_{self.client}_{self.batch}.pickle' -> 'test_apqa_1.pickle'
    """    
    state = SimpleNamespace()
    
    def _setStateIds(self):
        """ Sets the path to the pickle based on the attributes defined in state_ids.
            Called before loadState() and saveState() every time.
        """
        s = self.state_ids[0] + '_' + '_'.join([str(getattr(self, i)) for i in self.state_ids[1]]) + '.pickle'
        self._picklepath = (pickle_folder / s)

    def loadState(self):
        self._setStateIds()
        if self._picklepath.exists():
            with self._picklepath.open('rb') as p:
                self.state = pickle.load(p)

    def saveState(self):
        self._setStateIds()
        with self._picklepath.open('wb') as p:
            pickle.dump(self.state, p)
    
    @classmethod
    def persist(cls, func):
        """ Helper decorator to load the pickle and save after the method call.
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.loadState()
            func(self, *args, **kwargs)
            self.saveState()
        return wrapper
