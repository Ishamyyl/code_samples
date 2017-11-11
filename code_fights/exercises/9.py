#!/usr/bin/env python3

""" Write a function that takes a list of strings 
    AND a minimum length (number) 
    and returns only the strings that are longer than the provided number.
    Example Usage:
        # returns the list: ['baby', 'more', 'time']
        longer_than(3, 'hit', 'me', 'baby', 'one', 'more', 'time')
"""


from typing import Sequence


def longer_than(length, *args):
    if len(args) == 1 and isinstance(args[0], Sequence):
        args = args[0]
    return [w for w in args if len(w) > length]

def run():
    print(longer_than(3, 'hit', 'me', 'baby', 'one', 'more', 'time'))

if __name__ == '__main__':
    run()
