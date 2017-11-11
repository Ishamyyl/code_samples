#!/usr/bin/env python3

""" Write a function groupby that takes a key-function and a list. 
    The function should call key-function on all items in the list 
    and return a dictionary whose keys are the results of key-function 
    and values are all values from the list that productd that key.
    Example Usage:
        # returns: { h: ['hello', 'hi', 'help', 'here'], b: ['bye'] }
        groupby(lambda(s): s[0], 'hello', 'hi', 'help', 'bye', 'here')
"""


from collections import defaultdict


def groupby(key_func, *args):
    if len(args) == 1 and isinstance(args[0], Sequence):
        args = args[0]
    result = defaultdict(list)
    for i in args:
        result[key_func(i)].append(i)
    return result

def run():
    print(groupby(lambda s: s[0], 'hello', 'hi', 'help', 'bye', 'here'))

if __name__ == '__main__':
    run()
