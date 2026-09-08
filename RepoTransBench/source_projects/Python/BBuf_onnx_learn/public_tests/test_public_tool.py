import unittest
from tools import tool

class TestPublicToolFunctions(unittest.TestCase):

    def test_add(self):
        self.assertEqual(tool.add(5,7), 12)
        self.assertEqual(tool.add(-3,3), 0)
        self.assertEqual(tool.add(10,-10), 0)

    def test_sub(self):
        self.assertEqual(tool.sub(10,2), 8)
        self.assertEqual(tool.sub(-10,5), -15)

    def test_mul(self):
        self.assertEqual(tool.mul(7,3), 21)
        self.assertEqual(tool.mul(-4,2), -8)

    def test_div(self):
        self.assertEqual(tool.div(8,2), 4)
        with self.assertRaises(ZeroDivisionError):
            tool.div(-4,0)
    
    def test_tool_class(self):
        t = tool.Tool()
        self.assertEqual(t.multiply(4,-2), -8)
        self.assertEqual(t.identity(0), 0)
        self.assertTrue(callable(t.identity))

if __name__ == "__main__":
    unittest.main()