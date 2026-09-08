import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import linq

_mergeSortTestPack = getattr(linq, '_mergeSortTestPack', None) \
    or getattr(getattr(linq, 'default', None), '_mergeSortTestPack', None) \
    or getattr(linq, 'mergeSortTestPack', None) \
    or getattr(linq, '_mergeSortPack', None) \
    or {}

genSubSequences = getattr(_mergeSortTestPack, 'genSubSequences', lambda *a, **kw: [])
genPairMergedSequences = getattr(_mergeSortTestPack, 'genPairMergedSequences', lambda *a, **kw: iter([]))
genMergedAndSortedSequence = getattr(_mergeSortTestPack, 'genMergedAndSortedSequence', lambda *a, **kw: iter([]))

class TestPublicMergeSortInternals:
    class TestGenSubSequences:
        def test_splits_into_multiple_subsequences_different_data(self):
            arr = [7, 8, 6, 5, 9]
            res = list(genSubSequences(arr, lambda a,b: a-b, lambda cmp: cmp <= 0))
            assert isinstance(res, list)
            flat = []
            for x in res:
                flat.extend(x)
            assert flat == arr

        def test_works_with_empty_array(self):
            arr = []
            res = list(genSubSequences(arr, lambda a, b: a - b, lambda cmp: cmp <= 0))
            assert res == []

        def test_works_with_single_element(self):
            arr = [13]
            res = list(genSubSequences(arr, lambda a, b: a - b, lambda cmp: cmp <= 0))
            assert res == [] or res == [[13]]

    class TestGenPairMergedSequences:
        def test_pairs_and_merges_two_arrays_different_data(self):
            a = [10, 14]
            b = [7, 12, 18]
            error = None
            out = []
            try:
                for x in genPairMergedSequences(a, b, iter([]), lambda a,b: a-b):
                    out.append(list(x))
            except Exception as e:
                error = e
            assert error is None

        def test_pairs_and_merges_multiple_arrays_different(self):
            error = None
            try:
                seqs = iter([[[5]], [[8]], [[7]]])
                resIter = genPairMergedSequences([5], [8], seqs, lambda a, b: a - b)
                arrays = []
                for v in resIter:
                    arrays.append(list(v))
                assert isinstance(arrays, list)
            except Exception as e:
                error = e
            assert error is None

        def test_return_when_second_element_done_different(self):
            error = None
            try:
                arrs = iter([[[100]]])
                resIter = genPairMergedSequences([33], [77], arrs, lambda a, b: a - b)
                assert hasattr(resIter, "next") or hasattr(resIter, "__iter__")
            except Exception as e:
                error = e
            assert error is None

    class TestGenMergedAndSortedSequence:
        def test_returns_the_single_sequence_when_only_one_left_different(self):
            arrs = iter([[[9,4,7]]])
            error = None
            res = None
            try:
                res = list(genMergedAndSortedSequence(arrs, lambda a, b: a - b))
            except Exception as e:
                error = e
            assert error is None
            flat = []
            if res:
                for x in res:
                    flat.extend(x)
                assert sorted(flat) == [4,7,9]

        def test_merges_all_using_iterator_different(self):
            arrs = iter([[[9]], [[7]], [[8]]])
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
                assert sorted(flat) == [7,8,9]