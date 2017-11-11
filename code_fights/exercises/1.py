#!/usr/bin/env python3

""" Write a program that asks the user for a number (integer only) 
    and prints the sum of its digits
"""

def run():
    n = input('number (integer only) >')
    print(sum(int(d) for d in n))
    
if __name__ == '__main__':
    run() # run
