#!/usr/bin/env python3

""" Write a function that returns the multiplication of all input arguments. 
    The function should ignore non-numeric arguments.
    Example Usage:
        # returns 200:
        mymul('foo', 'bar', 10, 20)

        # returns 1:
        mymul()

        # returns 7:
        mymul(7)
"""


from numbers import Number
from operator import mul
from functools import reduce


def f(*args: Number, mul=mul) -> int:
    args = args or [1]
    return reduce(mul, (n for n in args if isinstance(n, Number)))

def run():
    try:
        print(f(1, 2, 3, 4))
        print(f(0, 1, 2, 3, 4))
        print(f(-1, 2, 3, 4))
        print(f(3.14159, 2))
        print(f(3/4, 4))
        print(f('foo', 'bar', 10, 20))
        print(f())
        print(f(7))
        # print(f(None))
        # print(f("asdf"))
        # print(f([]))
        # print(f("1234"))
        # print(f([1, 2, 3, 4]))
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    run()
