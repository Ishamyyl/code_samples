#!/usr/bin/env python3

""" Provided test file test_stack.py. 
    Write the module required to make the test pass:
        import unittest
        from lib import mystack

        class TestMyStack(unittest.TestCase):
            def setUp(self):
                mystack.add_item(10);
                mystack.add_item(20);
                mystack.add_item(22, 33);

            def test_flow(self):
                self.assertEqual(mystack.pop_item(), 33)
                self.assertEqual(mystack.pop_item(), 22)
                self.assertEqual(mystack.count_items(), 2)
                while mystack.pop_item(): pass

                self.assertEqual(mystack.count_items(), 0)
"""

import unittest
from lib_19 import mystack

class TestMyStack(unittest.TestCase):
    def setUp(self):
        mystack.add_item(10);
        mystack.add_item(20);
        mystack.add_item(22, 33);

    def test_flow(self):
        self.assertEqual(mystack.pop_item(), 33)
        self.assertEqual(mystack.pop_item(), 22)
        self.assertEqual(mystack.count_items(), 2)
        while mystack.pop_item(): pass

        self.assertEqual(mystack.count_items(), 0)

def test():
    unittest.main()

if __name__ == '__main__':
    test()
