import unittest
from src.gurugio_book.foreach import macro_if_foreach

class TestForeachPublic(unittest.TestCase):
    """Public tests for the macro_if_foreach function"""
    
    def test_macro_if_foreach_success_public(self):
        """Test successful cases of macro_if_foreach (public)"""
        ret = macro_if_foreach('c')
        self.assertEqual(ret, 3)
        ret = macro_if_foreach('d')
        self.assertEqual(ret, 4)
        ret = macro_if_foreach('e')
        self.assertEqual(ret, 5)
        ret = macro_if_foreach('a')
        self.assertEqual(ret, 1)
        ret = macro_if_foreach('b')
        self.assertEqual(ret, 2)
    
    def test_macro_if_foreach_invalid_public(self):
        """Test invalid cases of macro_if_foreach (public)"""
        ret = macro_if_foreach('y')
        self.assertEqual(ret, -1)
        ret = macro_if_foreach('%')
        self.assertEqual(ret, -1)

if __name__ == '__main__':
    unittest.main()
    print("test_foreach_public: OK")