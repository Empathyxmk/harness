import unittest
from tools.tool import add, sub, mul, div, Tool

class TestPublicToolsTool(unittest.TestCase):

    def test_basic_ops(self):
        self.assertEqual(add(20, 15), 35)
        self.assertEqual(sub(30, 25), 5)
        self.assertEqual(mul(6, 1), 6)
        self.assertEqual(div(81, 9), 9)

    def test_negative_values(self):
        self.assertEqual(sub(-10, 5), -15)
        self.assertEqual(mul(5, -5), -25)

    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError):
            div(-10, 0)

    def test_tool_multiply(self):
        t = Tool()
        self.assertEqual(t.multiply(9, 0), 0)

    def test_tool_identity(self):
        t = Tool()
        self.assertEqual(t.identity([1, "x", 3]), [1, "x", 3])

if __name__ == "__main__":
    unittest.main()