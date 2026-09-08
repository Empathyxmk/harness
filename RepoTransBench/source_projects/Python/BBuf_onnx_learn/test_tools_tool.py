# Same as 'test_tool.py' but for illustrative purposes, include different edge cases

import unittest
from tools.tool import add, sub, mul, div, Tool

class TestToolsTool(unittest.TestCase):

    def test_basic_ops(self):
        self.assertEqual(add(10, 5), 15)
        self.assertEqual(sub(10, 5), 5)
        self.assertEqual(mul(4, 0), 0)
        self.assertEqual(div(20, 4), 5)

    def test_negative_values(self):
        self.assertEqual(sub(-5, -5), 0)
        self.assertEqual(mul(-2, 3), -6)

    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError):
            div(1, 0)

    def test_tool_multiply(self):
        t = Tool()
        self.assertEqual(t.multiply(-1, 8), -8)

    def test_tool_identity(self):
        t = Tool()
        self.assertEqual(t.identity("abc"), "abc")

if __name__ == "__main__":
    unittest.main()