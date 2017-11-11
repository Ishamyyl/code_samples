'''
Created on Sep 20, 2016

@author: Ross.Hodapp
'''
from functools import wraps

class Stepper:
    """ Helper class to run steps in order. Useful for resuming a script where it last left off.
    """
    
    steps = []
    cur_step = 0
    
    def executeNextStep(self, *args, **kwargs):
        self.cur_step += 1
        self.steps[self.cur_step](*args, **kwargs)
    
    @classmethod
    def register(cls, func):
        cls.steps.append(func)
        print('register ' + str(cls.steps))
    
    @classmethod
    def step(cls, func):
        """ Decorator to register something as a step and in what order
        """
        @wraps(func)
        def wrapper(self):
            Stepper.register(func)
            return func
        return wrapper
