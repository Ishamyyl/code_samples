#!/usr/bin/env python3

""" Write a function that takes a number 
    and returns the sum of its digits. 
    Raise exception if argument of the wrong type was passed
"""


from numbers import Number


def f(n: Number) -> int:
    if isinstance(n, Number):
        return sum(int(d) for d in str(n) if d not in '.-ij')
    else:
        raise TypeError("gief Number pls")

def run():
    try:
        print(f(1234))
        print(f(0))
        print(f(-1234))
        print(f(3.14159))
        print(f(3/4))
        # print(f(None))
        # print(f("asdf"))
        # print(f([]))
        # print(f("1234"))
        # print(f([1, 2, 3, 4]))
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    run()
