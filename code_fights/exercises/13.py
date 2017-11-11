#!/usr/bin/env python3

""" Write a non-recursive implementation for the presented fib function using generators.
"""

def fib_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
        
def fib(n):
    g = fib_gen()
    for _ in range(n):
        next(g)
    return next(g)

def run():
    print(fib(10))

if __name__ == '__main__':
    run()
