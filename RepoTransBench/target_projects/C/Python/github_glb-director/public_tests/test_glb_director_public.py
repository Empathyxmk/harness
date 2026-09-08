import unittest
from src.glb_director.glb_director import sum, is_palindrome, max_of_three, average, factorial

class TestGlbDirectorPublic(unittest.TestCase):
    
    def test_sum_public(self):
        self.assertEqual(sum(3, 11), 14)
        self.assertEqual(sum(-2, 7), 5)
        self.assertEqual(sum(44, 77), 121)
        self.assertEqual(sum(-8, -12), -20)
    
    def test_is_palindrome_public(self):
        self.assertEqual(is_palindrome("evil olive"), 1)
        self.assertEqual(is_palindrome("civic"), 1)
        self.assertEqual(is_palindrome("palindrome"), 0)
        self.assertEqual(is_palindrome("openai"), 0)
    
    def test_max_of_three_public(self):
        self.assertEqual(max_of_three(4, 2, 5), 5)
        self.assertEqual(max_of_three(-5, -9, -2), -2)
        self.assertEqual(max_of_three(15, 32, 25), 32)
        self.assertEqual(max_of_three(77, 77, 77), 77)
    
    def test_average_public(self):
        arr1 = [2.0, 4.0, 6.0]
        self.assertEqual(average(arr1, 3), 4.0)
        
        arr2 = [9.5, 3.5]
        self.assertEqual(average(arr2, 2), 6.5)
        
        arr3 = [12.0]
        self.assertEqual(average(arr3, 1), 12.0)
        
        arr4 = [-12.0, -8.0, -16.0, -4.0]
        self.assertEqual(average(arr4, 4), -10.0)
    
    def test_factorial_public(self):
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(7), 5040)
        self.assertEqual(factorial(2), 2)

if __name__ == '__main__':
    unittest.main()