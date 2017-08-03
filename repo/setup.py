#!/usr/env/bin python3
'''
Created on Sep 14, 2016

@author: ross.hodapp
'''
from pathlib import Path

from setuptools import setup, find_packages


here = Path(__file__).parent

with (here / 'README').open('r') as readme:
    long_desc = readme.read()

setup(
    name='angelpoints',
    description='Tools for scripting for Angelpoints in Python',
    long_description=long_desc,
    url='redacted',
    author='Angelpoints Development',
    author_email='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database',
        'Topic :: Office/Business',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
      
    use_scm_version=True,  # Automatic version updates based on tags
    setup_requires=['setuptools_scm'],
    
    packages=find_packages(),  # Automatically specifies the packages used
    include_package_data=True,  # Uses MANIFEST.in to specify which non-code data to include
    
    test_suite='angelpoints.tests',
    
    install_requires=[
        'mysql-connector-python-rf',  # official Oracle MySQL Python wrapper 
    ],
      
    entry_points={
        'console_scripts': [
            'run_tests = angelpoints.tests.main:TestUnittests',
            'batch_export = angelpoints.profs.scripts.batch_send:BatchExportScript'
        ]
    }
)
