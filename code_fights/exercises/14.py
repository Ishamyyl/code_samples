#!/usr/bin/env python3

""" Write a decorator called returns that checks that a function returns expected argument type.

    Usage example:
        @returns(str)
        def same(word)
          return word

        # works:
        same('hello')

        # raise AssertionError:
        same(10)
"""


from functools import wraps
from itertools import starmap
from inspect import signature


def type_checked(func):
    #assert len(signature(func).parameters) == len(decorator.accepts), "incorrect number of arguments to @accepts"
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        b = sig.bind(*args, **kwargs)
        print(b)
        #print(sig.parameters['n'].annotation, sig.return_annotation)
        r = func(*args, **kwargs)
        #assert isinstance(r, decorator.returns), "incorrect return types matching @returns"
        return r
    return wrapper

def returns(type_check):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            r = func(*args, **kwargs)
            assert isinstance(r, decorator.returns), "incorrect return types matching @returns"
            return r
        return wrapper
    decorator.returns = type_check
    return decorator

def accepts(*args):
    def decorator(func):
        assert len(signature(func).parameters) == len(decorator.accepts), "incorrect number of arguments to @accepts"
        @wraps(func)
        def wrapper(*args, **kwargs):
            assert all(starmap(isinstance, zip(args, decorator.accepts))), "incorrect argument types matching @accepts"
            return func(*args, **kwargs)
        return wrapper
    decorator.accepts = args
    return decorator

#@accepts(int)
#@returns(str)
@type_checked
def intToStr(n: int) -> str:
    return str(n)

def run():
    print(intToStr(10))

if __name__ == '__main__':
    run()
