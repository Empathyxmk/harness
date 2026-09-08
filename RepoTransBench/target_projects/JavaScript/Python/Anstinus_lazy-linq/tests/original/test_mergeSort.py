import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from linq import _mergeSortTestPack as algo

def iterToArray(iterable):
    result = []
    for elem in iterable:
        result.append(elem)
    return result

class TestSortAlgo:

    class TestGenSubSequences:
        def test_should_divide_sequence_by_natural_order(self):
            data = [2, 1, 3, 6, 4, 2, 2, 5, 3, 4]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: x - y, lambda x: x <= 0))
            assert result == [
                [2],
                [1, 3, 6],
                [4],
                [2, 2, 5],
                [3, 4]
            ]

        def test_should_divide_according_to_comp(self):
            data = [2, 1, 3, 6, 4, 2, 2, 5, 3, 4]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: y - x, lambda x: x <= 0))
            assert result == [
                [2, 1],
                [3],
                [6, 4, 2, 2],
                [5, 3],
                [4]
            ]

        def test_should_divide_according_to_compGroupChecker(self):
            data = [2, 1, 3, 6, 4, 2, 2, 5, 3, 4]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: x - y, lambda x: x == 0))
            assert result == [
                [2],
                [1],
                [3],
                [6],
                [4],
                [2, 2],
                [5],
                [3],
                [4]
            ]

        def test_when_sequence_is_empty_should_return_empty_sequence(self):
            data = []
            result = iterToArray(algo.genSubSequences(data, lambda x, y: x - y, lambda x: x <= 0))
            assert len(result) == 0

        def test_should_divide_undefined_separately(self):
            data = [2, 1, 3, None, 6, 4, 2, 2, 5, 3, 4]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0), lambda x: x <= 0))
            assert result == [
                [2],
                [1, 3],
                [None],
                [6],
                [4],
                [2, 2, 5],
                [3, 4]
            ]

        def test_should_divide_multiple_undefined_separately(self):
            data = [2, 1, 3, None, None, 6, 4, 2, 2, 5, 3, 4]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0), lambda x: x <= 0))
            assert result == [
                [2],
                [1, 3],
                [None],
                [None],
                [6],
                [4],
                [2, 2, 5],
                [3, 4]
            ]

        def test_should_divide_invalid_value_separately(self):
            data = [2, 1, 3, None, 'abc', 6, 4, 2, 2, 5, 3, 4]
            result = iterToArray(algo.genSubSequences(data,
                lambda x, y: (x if isinstance(x, (int, float)) else 0) - (y if isinstance(y, (int, float)) else 0),
                lambda x: x <= 0))
            assert result == [
                [2],
                [1, 3],
                [None],
                ['abc'],
                [6],
                [4],
                [2, 2, 5],
                [3, 4]
            ]

    class TestGenTwoMergedSequence:
        def test_should_merge(self):
            data1 = [1, 3, 4]
            data2 = [2, 4, 5]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: x - y))
            assert result == [1, 2, 3, 4, 4, 5]

        def test_should_merge_according_to_comp(self):
            data1 = [4, 3, 1]
            data2 = [5, 4, 2]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: y - x))
            assert result == [5, 4, 4, 3, 2, 1]

        def test_should_work_fine_when_one_sequence_is_empty(self):
            data1 = [1, 3, 4]
            data2 = [2, 4, 5]
            result = iterToArray(algo.genTwoMergedSequence([], data2, lambda x, y: x - y))
            assert result == [2, 4, 5]
            result2 = iterToArray(algo.genTwoMergedSequence(data1, [], lambda x, y: x - y))
            assert result2 == [1, 3, 4]

        def test_should_merge_undefined_alone(self):
            data1 = [1, 3, 4]
            data2 = [None]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [None, 1, 3, 4]

        def test_should_merge_undefined_mixed(self):
            data1 = [2, 4, None]
            data2 = [1, 3]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [1, 2, 3, 4, None]

        def test_should_merge_undefined_mixed_in_middle(self):
            data1 = [2, None, 4]
            data2 = [1, 3]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [1, 2, None, 3, 4]

        def test_should_merge_undefined_in_head_of_array(self):
            data1 = [None, 1]
            data2 = [1, 3]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [None, 1, 1, 3]

    class TestGenMergedAndSortedSequence:
        def test_when_sequence_count_is_even_should_merge_correctly(self):
            data = [[1, 2], [1, 4], [2], [1, 3]]
            result = iterToArray(algo.genMergedAndSortedSequence(iter(data), lambda x, y: x - y))
            assert result == [1, 1, 1, 2, 2, 3, 4]

        def test_when_sequence_count_is_odd_should_merge_correctly(self):
            data = [[1, 2], [1, 4], [2]]
            result = iterToArray(algo.genMergedAndSortedSequence(iter(data), lambda x, y: x - y))
            assert result == [1, 1, 2, 2, 4]

        def test_when_sequence_count_is_2_should_merge_correctly(self):
            data = [[1, 2], [1, 4]]
            result = iterToArray(algo.genMergedAndSortedSequence(iter(data), lambda x, y: x - y))
            assert result == [1, 1, 2, 4]

        def test_when_sequence_count_is_1_should_return_it_directly(self):
            data = [[1, 2]]
            result = iterToArray(algo.genMergedAndSortedSequence(iter(data), lambda x, y: x - y))
            assert result == [1, 2]

        def test_when_sequence_count_is_0_should_return_empty_sequence(self):
            data = []
            result = iterToArray(algo.genMergedAndSortedSequence(iter(data), lambda x, y: x - y))
            assert len(result) == 0

        def test_when_some_sequence_is_empty_should_merge_without_error(self):
            data = [[1, 2], [1, 4], [], []]
            result = iterToArray(algo.genMergedAndSortedSequence(iter(data), lambda x, y: x - y))
            assert result == [1,1,2,4]

        def test_when_sequence_has_undefined_should_merge_correctly(self):
            data = [[1,2], [None], [1,3]]
            result = iterToArray(algo.genMergedAndSortedSequence(iter(data), lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [None, 1, 1, 2, 3]

    class TestGenMergeSort:
        def test_should_sort_correctly(self):
            data = [3,2,7,9,5,0]
            result = iterToArray(algo.genMergeSort(data, lambda x, y: x - y))
            assert result == [0,2,3,5,7,9]

        def test_when_sequence_is_empty_should_return_empty_sequence(self):
            data = []
            result = iterToArray(algo.genMergeSort(data, lambda x, y: x - y))
            assert len(result) == 0

        def test_when_sequence_contains_only_1_element_should_work_fine(self):
            data = [3]
            result = iterToArray(algo.genMergeSort(data, lambda x, y: x - y))
            assert result == [3]

        def test_when_sequence_contains_only_2_elements_should_work_fine(self):
            data = [6,2]
            result = iterToArray(algo.genMergeSort(data, lambda x, y: x - y))
            assert result == [2,6]

        def test_when_comp_is_provided_should_sort_by_it(self):
            data = [1,3,2]
            result = iterToArray(algo.genMergeSort(data, lambda x, y: y - x))
            assert result == [3,2,1]

        def test_should_be_stable(self):
            data = ['bd','bb','cc','aa','ab']
            result = iterToArray(algo.genMergeSort(data, lambda x, y: -1 if x[0] < y[0] else (0 if x[0]==y[0] else 1)))
            assert result == ['aa','ab','bd','bb','cc']

        def test_should_sort_correctly_with_undefined(self):
            data = [3,2,7,9,None,5,0]
            result = iterToArray(algo.genMergeSort(data, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [None,0,2,3,5,7,9]