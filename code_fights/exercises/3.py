#!/usr/bin/env python3


""" Given the following input,
    create a CSV file from the data as follows:

    interface,inet,status
    lo0,127.0.0.1,
    gif0,,
    en0,10.176.85.19,active
    en1,,inactive
    p2p0,,inactive  
"""

from csv import DictWriter
from pathlib import Path
from collections import defaultdict

fieldnames = ['interface', 'inet', 'status']

def run():

    input = """lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
    options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
    inet 127.0.0.1 netmask 0xff000000 
    inet6 ::1 prefixlen 128 
    inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1 
    nd6 options=201<PERFORMNUD,DAD>
gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
    ether f4:0f:24:29:df:4d 
    inet6 fe80::1cb5:1689:1826:cc7b%en0 prefixlen 64 secured scopeid 0x4 
    inet 10.176.85.19 netmask 0xffffff00 broadcast 10.176.85.255
    nd6 options=201<PERFORMNUD,DAD>
    media: autoselect
    status: active
en1: flags=963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX> mtu 1500
    options=60<TSO4,TSO6>
    ether 06:00:58:62:a3:00 
    media: autoselect <full-duplex>
    status: inactive
p2p0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> mtu 2304
    ether 06:0f:24:29:df:4d 
    media: autoselect
    status: inactive
"""

    input = iter(input.splitlines())
    with Path('3_out.csv').open('w') as fo:
        writer = DictWriter(fo, fieldnames)
        writer.writeheader()
        ifcs = []  # collect the interfaces into list called ifcs
        for line in input:
            # identify and group the input lines
            if not line.startswith(' '):    # this is a new interface...
                ifcs.append([line])         # ...so create a new list to represent it
            else:                           # a subline is defined by having space-indents at the beginning
                ifcs[-1].append(line)       # add it to the end of the list representing the last interface
        for ifc in ifcs:
            # process the identified groups of input lines
            row = defaultdict(str)
            ifc = iter(ifc)
            row['interface'] = next(ifc).split(':', maxsplit=1)[0].strip()  # the first item in the interface list is always the 'new interface' line, so get the interface name from it
            for line in ifc:  # loop over the remaining lines...
                info = line.split()  # ...which is info about the interface
                opt = info[0].strip(':')
                
                # it's coincidence that the attributes we want from the info line are in the same place
                if 'inet' == opt:
                    row[opt] = info[1]
                if 'status' == opt:
                    row[opt] = info[1]
                # if opt in ['inet', 'status']:
                #     row[opt] = info[1]
            writer.writerow(row)

if __name__ == '__main__':
    run()
