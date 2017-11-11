'''
Created on Sep 15, 2016

@author: ross.hodapp
'''
from csv import DictWriter


class Reporter:
    
    def __init__(self, csv_class=DictWriter, delimiter=','):
        """ Optionally provide the CSV Writer class, defaults to DictWriter, and the delimiter, defaults to ','.
        """
        self.delimiter = delimiter
        self.csv_class = csv_class

    def writeReport(self, data, file_path, prereport_hooks=[]):
        """ Write DATA, to a FILE_PATH, which shall be a Path() object. The DATA should be in an acceptable format for your given CSV Writer.
            Optionally provide PREREPORT_HOOKS, which shall be a list of methods that accept 1 argument which will be the line to pre-process.
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w', newline='\n') as fp:
            writer = self.csv_class(fp, self.current_fieldnames)
            writer.writeheader()
            for line in data:
                if prereport_hooks:
                    for hook in prereport_hooks:
                        line = hook(line)
                writer.writerow(line)
