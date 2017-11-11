#!/usr/bin/env python3

""" Calculation in the following fib function may take a long time. 
    Implement a Decorator that remembers old calculations
    so the function won't calculate a fib value more than once. 
    
    Program Code:
        @memoize
        def fib(n):
            print("fib({})".format(n))
            if n <= 2:
                return 1
            else:
                return fib(n-1) + fib(n-2)
                
    Expected Output:
        fib(10)
        fib(9)
        fib(8)
        fib(7)
        fib(6)
        fib(5)
        fib(4)
        fib(3)
        fib(2)
        fib(1)
        55
"""


from functools import wraps, lru_cache


def memoize(func):
    @wraps(func)
    def wrapper(*args):
        d = wrapper.cache
        if args in d:
            return d[args]
        r = func(*args)
        d[args] = r
        return r
    wrapper.cache = {}
    return wrapper

@memoize
def fib(n):
    print("fib({})".format(n))
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

@lru_cache()
def fib2(n):
    print("fib({})".format(n))
    if n <= 2:
        return 1
    else:
        return fib2(n-1) + fib2(n-2)

def run():
    print(fib(10))
    print('-----')
    print(fib2(10))

if __name__ == '__main__':
    run()
