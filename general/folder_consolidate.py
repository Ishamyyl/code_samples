#!/usr/bin/env python

##
# The goal of this script was to consolidate a bunch of folders together based on a Identifier in the folder. 
# The folders almost always had the same naming convention. 
##

import os
import re
from pathlib import Path

s = Path( u"redacted")  # source
os.chdir( s.as_posix())

d = (s / '..' / 'result')  # destination
if not d.exists():
    d.mkdir()

i = 0
for file in list( f for f in s.glob( '**/*') if not f.is_dir() and re.search( '^[A-Z]{2}[0-9]{3,4}(\s|$)', f.parts[-2])):  # loop through each file
    fund_id_dir = (d / file.parts[-2][:6].strip())  # get the ID from the parent folder
    i += 1
    if not fund_id_dir.exists():
        fund_id_dir.mkdir()
    try:
        os.rename( file.as_posix(), (fund_id_dir / file.name).as_posix())  # mv file to destination folder
    except FileExistsError as fee:
        os.rename( file.as_posix(), (fund_id_dir / "{f}_{i}".format( f=file.name, i=i)).as_posix())  # if the file already exists, append a unique number to it
