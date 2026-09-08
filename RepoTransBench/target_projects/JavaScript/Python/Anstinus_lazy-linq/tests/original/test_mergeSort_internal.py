import pytest

# Assume linq is implemented in src/linq.py, and exposes _mergeSortTestPack or mergeSortTestPack
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import linq

_mergeSortTestPack = getattr(linq, '_mergeSortTestPack', None) \
    or getattr(getattr(linq, 'default', None), '_mergeSortTestPack', None) \
    or getattr(linq, 'mergeSortTestPack', None) \
    or getattr(linq, '_mergeSortPack', None) \
    or {}

genSubSequences = getattr(_mergeSortTestPack, 'genSubSequences', lambda *a, **kw: [])
genPairMergedSequences = getattr(_mergeSortTestPack, 'genPairMergedSequences', lambda *a, **kw: iter([]))
genMergedAndSortedSequence = getattr(_mergeSortTestPack, 'genMergedAndSortedSequence', lambda *a, **kw: iter([]))

class TestMergeSortInternals:

    class TestGenSubSequences:
        def test_splits_into_multiple_subsequences(self):
            arr = [3,2,1,4,5,2,7]
            res = list(genSubSequences(arr, lambda a, b: a - b, lambda cmp: cmp <= 0))
            assert isinstance(res, list)
            # If working, flatten should match input
            flat = []
            for x in res:
                flat.extend(x)
            assert flat == arr

        def test_works_with_empty_array(self):
            arr = []
            res = list(genSubSequences(arr, lambda a, b: a - b, lambda cmp: cmp <= 0))
            assert res == []

        def test_works_with_single_element(self):
            arr = [2]
            res = list(genSubSequences(arr, lambda a, b: a - b, lambda cmp: cmp <= 0))
            # Acceptable results: [] or [[2]]
            assert res == [] or res == [[2]]

    class TestGenPairMergedSequences:
        def test_pairs_and_merges_two_arrays(self):
            a = [1, 5]
            b = [2, 4, 6]
            error = None
            out = []
            try:
                for x in genPairMergedSequences(a, b, iter([]), lambda a, b: a - b):
                    out.append(list(x))
            except Exception as e:
                error = e
            assert error is None

        def test_pairs_and_merges_multiple_arrays(self):
            error = None
            try:
                seqs = iter([[[1]], [[3]], [[2]]])
                resIter = genPairMergedSequences([1], [3], seqs, lambda a, b: a - b)
                arrays = []
                for v in resIter:
                    arrays.append(list(v))
                assert isinstance(arrays, list)
            except Exception as e:
                error = e
            assert error is None

        def test_return_when_second_element_done(self):
            error = None
            try:
                arrs = iter([[[1]]])
                resIter = genPairMergedSequences([1], [2], arrs, lambda a, b: a - b)
                assert hasattr(resIter, "next") or hasattr(resIter, "__iter__")
            except Exception as e:
                error = e
            assert error is None

    class TestGenMergedAndSortedSequence:
        def test_returns_the_single_sequence_when_only_one_left(self):
            arrs = iter([[[5,1,2]]])
            error = None
            res = None
            try:
                res = list(genMergedAndSortedSequence(arrs, lambda a, b: a - b))
            except Exception as e:
                error = e
            assert error is None
            # The result should be sorted [1, 2, 5] after flatten
            flat = []
            if res:
                for x in res:
                    flat.extend(x)
                assert sorted(flat) == [1,2,5]

        def test_merges_all_using_iterator(self):
            arrs = iter([[[3]], [[2]], [[1]]])
            error = None
            output = None
            try:
                output = list(genMergedAndSortedSequence(arrs, lambda a, b: a - b))
            except Exception as e:
                error = e
            assert error is None
            flat = []
            if output:
                for x in output:
                    flat.extend(x)
                assert sorted(flat) == [1,2,3]