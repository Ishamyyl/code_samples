#!/usr/bin/env python3

""" The following code assumes a class named Widget 
    which represents a thing that needs to be built. 
    Building a widget should automatically trigger a build on all its dependencies. 
    
    Implement Widget so the following code works:
        luke    = Widget("Luke")
        hansolo = Widget("Han Solo")
        leia    = Widget("Leia")
        yoda    = Widget("Yoda")
        padme   = Widget("Padme Amidala")
        anakin  = Widget("Anakin Skywalker")
        obi     = Widget("Obi-Wan")
        darth   = Widget("Darth Vader")
        _all    = Widget("All")


        luke.add_dependency(hansolo, leia, yoda)
        leia.add_dependency(padme, anakin)
        obi.add_dependency(yoda)
        darth.add_dependency(anakin)

        _all.add_dependency(luke, hansolo, leia, yoda, padme, anakin, obi, darth)
        _all.build()
        # code should print: Han Solo, Padme Amidala, Anakin Skywalker, Leia, Yoda, Luke, Obi-Wan, Darth Vader
        # (can print with newlines in between modules)
"""


class Widget:
    def __init__(self, name):
        self.name = name
        self.dependencies = []
        self.built = False
        
    def add_dependency(self, *names):
        self.dependencies.extend(names)
        
    def _build(self):
        if not self.built:
            print(self.name)
            self.built = True
        
    def build(self):
        for d in self.dependencies:
            d.build()
        self._build()

def run():
    luke    = Widget("Luke")
    hansolo = Widget("Han Solo")
    leia    = Widget("Leia")
    yoda    = Widget("Yoda")
    padme   = Widget("Padme Amidala")
    anakin  = Widget("Anakin Skywalker")
    obi     = Widget("Obi-Wan")
    darth   = Widget("Darth Vader")
    _all    = Widget("All")


    luke.add_dependency(hansolo, leia, yoda)
    leia.add_dependency(padme, anakin)
    obi.add_dependency(yoda)
    darth.add_dependency(anakin)
    
    _all.add_dependency(luke, hansolo, leia, yoda, padme, anakin, obi, darth)
    _all.build()

if __name__ == '__main__':
    run()
