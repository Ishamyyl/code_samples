#!/usr/bin/env python3

""" Write a python program that calls ifconfig and splits its output to files according to the network interfaces it finds.

    For example given the following ifconfig output:
        en3: flags=8963 mtu 1500
                options=60
                ether 32:00:18:24:c0:00
                media: autoselect 
                status: inactive
        p2p0: flags=8843 mtu 2304
                ether 06:38:35:47:96:24
                media: autoselect
                status: inactive
                
    Program should create 2 files named: en3 and p2p0, saving the first block to file en3 and the second one to p2p0.
"""


from subprocess import check_output
from pathlib import Path


def run():
    interfaces = [i.split()[0] for i in check_output('ifconfig -s', universal_newlines=True, shell=True).splitlines()[1:]]
    for ifc in interfaces:
        with Path(ifc).open('w') as f:
            f.write(check_output('ifconfig {ifc}'.format(ifc=ifc), universal_newlines=True, shell=True))

if __name__ == '__main__':
    run()
