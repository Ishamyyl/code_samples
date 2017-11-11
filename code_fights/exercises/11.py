#!/usr/bin/env python3

""" Write a Decorator named after5 that will ignore the decorated function in the first 5 times it is called. 

    Example Usage:
        @after5
        def doit(): print("Yo!")

        # ignore the first 5 calls
        doit()
        doit()
        doit()
        doit()
        doit()

        # so only print yo once
        doit()
"""


from functools import wraps


def after5(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if wrapper.calls >= 5:
            func(*args, **kwargs)
        wrapper.calls += 1
    wrapper.calls = 0
    return wrapper

@after5
def run():
    print('Yo!')

if __name__ == '__main__':
    run()
    run()
    run()
    run()
    run()
    
    run()
