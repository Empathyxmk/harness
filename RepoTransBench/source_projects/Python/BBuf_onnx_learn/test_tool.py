# Attempt to only use unittest.mock and standard libraries, avoid flexmock/pytest plugins

import unittest
import sys
import types

from tools import tool

class TestToolFunctions(unittest.TestCase):

    def test_add(self):
        self.assertEqual(tool.add(1,2), 3)
        self.assertEqual(tool.add(-2,2), 0)
        self.assertEqual(tool.add(0,0), 0)

    def test_sub(self):
        self.assertEqual(tool.sub(3,2), 1)
        self.assertEqual(tool.sub(-1,1), -2)

    def test_mul(self):
        self.assertEqual(tool.mul(3,2), 6)
        self.assertEqual(tool.mul(0,8), 0)

    def test_div(self):
        self.assertEqual(tool.div(6,3), 2)
        with self.assertRaises(ZeroDivisionError):
            tool.div(3,0)
    
    def test_tool_class(self):
        t = tool.Tool()
        self.assertEqual(t.multiply(2,3), 6)
        self.assertEqual(t.identity(10), 10)
        self.assertTrue(callable(t.identity))

if __name__ == "__main__":
    unittest.main()