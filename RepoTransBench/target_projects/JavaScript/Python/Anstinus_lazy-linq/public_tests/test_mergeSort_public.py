import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from linq import _mergeSortTestPack as algo

def iterToArray(iterable):
    return [elem for elem in iterable]

class TestPublicSortAlgo:
    class TestGenSubSequences:
        def test_should_divide_sequence_by_natural_order_different_data(self):
            data = [9, 8, 10, 13, 7, 5, 4, 11, 8, 10]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: x - y, lambda x: x <= 0))
            assert result == [
                [9],
                [8, 10, 13],
                [7],
                [5, 4, 11],
                [8, 10]
            ]

        def test_should_divide_according_to_comp_different_data(self):
            data = [11, 10, 14, 18, 15, 11, 12, 14, 12, 16]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: y - x, lambda x: x <= 0))
            assert result == [
                [11, 10],
                [14],
                [18, 15, 11, 12],
                [14, 12],
                [16]
            ]

        def test_should_divide_according_to_compGroupChecker_different_data(self):
            data = [10, 10, 11, 13, 13, 14, 15, 15, 16, 17]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: x - y, lambda x: x == 0))
            assert result == [
                [10, 10],
                [11],
                [13, 13],
                [14],
                [15, 15],
                [16],
                [17]
            ]

        def test_when_sequence_is_empty_should_return_empty_sequence(self):
            data = []
            result = iterToArray(algo.genSubSequences(data, lambda x, y: x - y, lambda x: x <= 0))
            assert len(result) == 0

        def test_should_divide_undefined_separately_different(self):
            data = [18, 17, 15, None, 20, 12, 13, 10]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0), lambda x: x <= 0))
            assert result == [
                [18],
                [17, 15],
                [None],
                [20],
                [12, 13],
                [10]
            ]

        def test_should_divide_multiple_undefined_separately_different(self):
            data = [9, None, None, 5, 4, 6]
            result = iterToArray(algo.genSubSequences(data, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0), lambda x: x <= 0))
            assert result == [
                [9],
                [None],
                [None],
                [5],
                [4, 6]
            ]

        def test_should_divide_invalid_value_separately_different(self):
            data = [10, None, 'xyz', 3, 6]
            result = iterToArray(algo.genSubSequences(data,
                        lambda x, y: (x if isinstance(x, (int, float)) else 0) - (y if isinstance(y, (int, float)) else 0),
                        lambda x: x <= 0))
            assert result == [
                [10],
                [None],
                ['xyz'],
                [3, 6]
            ]

    class TestGenTwoMergedSequence:
        def test_should_merge_different_data(self):
            data1 = [5, 12, 15]
            data2 = [7, 13, 17]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: x - y))
            assert result == [5, 7, 12, 13, 15, 17]

        def test_should_merge_according_to_comp_different_data(self):
            data1 = [15, 12, 5]
            data2 = [19, 15, 10]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: y - x))
            assert result == [19, 15, 15, 12, 10, 5]

        def test_should_work_fine_when_one_sequence_is_empty_different(self):
            data1 = [8, 14]
            data2 = [6, 9, 20]
            result = iterToArray(algo.genTwoMergedSequence([], data2, lambda x, y: x - y))
            assert result == [6, 9, 20]
            result2 = iterToArray(algo.genTwoMergedSequence(data1, [], lambda x, y: x - y))
            assert result2 == [8, 14]

        def test_should_merge_undefined_alone_different(self):
            data1 = [20, 25]
            data2 = [None]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [None, 20, 25]

        def test_should_merge_undefined_mixed_different(self):
            data1 = [13, 15, None]
            data2 = [9, 20]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [9, 13, 15, 20, None]

        def test_should_merge_undefined_mixed_in_middle_different(self):
            data1 = [5, None, 12]
            data2 = [1, 9]
            result = iterToArray(algo.genTwoMergedSequence(data1, data2, lambda x, y: (x if x is not None else 0) - (y if y is not None else 0)))
            assert result == [1, 5, 9, 12, None]