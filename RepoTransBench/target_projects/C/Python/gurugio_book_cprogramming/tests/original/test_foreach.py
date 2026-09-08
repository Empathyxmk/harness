import unittest
from src.gurugio_book.foreach import macro_if_foreach

class TestForeach(unittest.TestCase):
    """Tests for the macro_if_foreach function translated from test_foreach.c"""
    
    def test_macro_if_foreach_success(self):
        """Test successful cases of macro_if_foreach"""
        ret = macro_if_foreach('a')
        self.assertEqual(ret, 1)
        ret = macro_if_foreach('b')
        self.assertEqual(ret, 2)
        ret = macro_if_foreach('c')
        self.assertEqual(ret, 3)
        ret = macro_if_foreach('d')
        self.assertEqual(ret, 4)
        ret = macro_if_foreach('e')
        self.assertEqual(ret, 5)
    
    def test_macro_if_foreach_invalid(self):
        """Test invalid cases of macro_if_foreach"""
        ret = macro_if_foreach('z')
        self.assertEqual(ret, -1)
        ret = macro_if_foreach(0)
        self.assertEqual(ret, -1)

if __name__ == '__main__':
    unittest.main()
    print("test_foreach: OK")