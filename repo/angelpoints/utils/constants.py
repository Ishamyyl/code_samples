'''
Created on Sep 13, 2016

@author: ross.hodapp
'''
from os import name as os_name
from pathlib import Path
import platform


app_name = 'redacted'

if os_name == 'posix':
    prog_data_folder = Path('redacted')
elif os_name == 'nt':
    prog_data_folder = Path.home()
else:
    raise ValueError("You're not Windows or Posix... (???) O_O")
prog_data_folder = (prog_data_folder / app_name)

batches_folder = (prog_data_folder / 'batches')
pickle_folder = (prog_data_folder / 'picklejar')

if not batches_folder.exists():
    batches_folder.mkdir(parents=True)
if not pickle_folder.exists():
    pickle_folder.mkdir(parents=True)

hostname = platform.node()

db_user = 'redacted'
db_pass = 'redacted'
from settings_local import *
