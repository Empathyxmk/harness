import unittest
from functools import partial

from p_tqdm.p_tqdm import p_map, p_imap

def combine_values(a, b=2, c=1):
    return a + b*3 + c*4

class Test_p_map_public(unittest.TestCase):
    func = staticmethod(p_map)
    generator = False
    ordered = True

    def test_two_lists_and_one_single(self):
        # arr1 (used as b), arr2 (a), single (c)
        array_1 = [2, 8, 14]
        array_2 = [7, 1, 4]
        single = 5
        # To test a=array_2, b=array_1, c=single
        result = self.func(partial(combine_values, c=single), array_2, array_1)
        if self.generator:
            result = list(result)

        # combine_values(a=array_2, b=array_1, c=single)
        correct_array = [
            array_2[0] + array_1[0]*3 + single*4,
            array_2[1] + array_1[1]*3 + single*4,
            array_2[2] + array_1[2]*3 + single*4,
        ]
        if self.ordered:
            self.assertEqual(correct_array, result)

    def test_one_list_and_two_singles(self):
        # pass array as a, single_1 is b, single_2 is c
        array = [20, 25, 28]
        single_1 = 4
        single_2 = 6
        # combine_values(a, b, c)
        result = self.func(partial(combine_values, b=single_1, c=single_2), array)
        if self.generator:
            result = list(result)

        # array + single_1*3 + single_2*4
        correct_array = [v + single_1*3 + single_2*4 for v in array]
        if self.ordered:
            self.assertEqual(correct_array, result)

    def test_single_list(self):
        array = [5, 15, 35]
        result = self.func(combine_values, array)
        if self.generator:
            result = list(result)
        correct = [v + 2*3 + 1*4 for v in array]
        if self.ordered:
            self.assertEqual(correct, result)

    def test_multiple_lists(self):
        # Testing combine_values(a, b, c) with three lists
        array1 = [5, 9, 13]
        array2 = [2, 4, 6]
        array3 = [3, 5, 7]
        result = self.func(combine_values, array1, array2, array3)
        if self.generator:
            result = list(result)
        # a, b, c = array1, array2, array3
        correct = [a + b*3 + c*4 for a,b,c in zip(array1, array2, array3)]
        if self.ordered:
            self.assertEqual(correct, result)

    def test_different_func(self):
        def cube_sum(a, b):
            return (a + b) ** 3
        list1 = [1,3,5]
        list2 = [2,4,6]
        result = self.func(cube_sum, list1, list2)
        if self.generator:
            result = list(result)
        self.assertEqual([(1+2)**3, (3+4)**3, (5+6)**3], result)

class Test_p_imap_public(Test_p_map_public):
    func = staticmethod(p_imap)
    generator = True

    # (inherits tests with generator mode)