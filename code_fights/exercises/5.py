#!/usr/bin/env python3

""" Write a python program that takes a list of file extensions 
    and prints all the files from the current directory matching the extension given.
    
    The following extensions and meaning should be supported:
        c should find and print all .c and .h file names
        py should find and print all .py and .pyc file names
        pl should find and print all .pl and .pm file names
    
    Bonus: Read extension and meaning from a configuration file.
"""


from pathlib import Path
from configparser import ConfigParser
import sys


ini_file = """[ext]
c = *.[ch]
py = *.py*
pl = *.p[lm]
"""

def run():
    config = ConfigParser()
    config.read_string(ini_file)
    files = Path( '.').glob( config.get( 'ext', sys.argv[1]))
    for f in files:
        print(f)

if __name__ == '__main__':
    run()
