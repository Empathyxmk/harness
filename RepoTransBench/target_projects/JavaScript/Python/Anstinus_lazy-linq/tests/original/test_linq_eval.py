import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import linq

# Install asEnumerable for list objects if needed
if hasattr(linq, "installAsEnumerable"):
    linq.installAsEnumerable()

class TestLinqEvalMembers:

    def test_all_should_throw_when_pred_not_function(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.all()
        with pytest.raises(Exception):
            data.all(1)
        with pytest.raises(Exception):
            data.all({})
    
    def test_all_with_non_empty_sequence(self):
        data = linq.range(1, 3)
        assert data.all(lambda x: x > 0) is True
        assert data.all(lambda x: x < 0) is False
        assert data.all(lambda x: x > 1) is False

    def test_all_with_empty_sequence(self):
        assert linq.empty().all(lambda x: False) is True

    def test_any_with_non_empty_sequence(self):
        data = linq.range(1, 3)
        assert data.any(lambda x: x > 0) is True
        assert data.any(lambda x: x < 0) is False
        assert data.any(lambda x: x > 1) is True
        assert data.any() is True

    def test_any_with_empty_sequence(self):
        assert linq.empty().any(lambda x: True) is False
        assert linq.empty().any() is False

    def test_singleOrDefault_with_empty_sequence(self):
        data = linq.empty()
        assert data.singleOrDefault() is None
        assert data.singleOrDefault(lambda x: True) is None

    def test_singleOrDefault_with_one_element_sequence(self):
        data = linq.range(1, 1)
        assert data.singleOrDefault() == 1
        assert data.singleOrDefault(lambda x: x >= 1) == 1
        assert data.singleOrDefault(lambda x: x >= 4) is None

    def test_singleOrDefault_with_more_than_one_element(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.singleOrDefault()
        assert data.singleOrDefault(lambda x: x % 2 == 0) == 2
        with pytest.raises(Exception):
            data.singleOrDefault(lambda x: x % 2 != 0)
        assert data.singleOrDefault(lambda x: x >= 4) is None

    def test_single_with_empty_sequence(self):
        data = linq.empty()
        with pytest.raises(Exception):
            data.single()
        with pytest.raises(Exception):
            data.single(lambda x: True)

    def test_single_with_one_element(self):
        data = linq.range(1, 1)
        assert data.single() == 1
        assert data.single(lambda x: x >= 1) == 1
        with pytest.raises(Exception):
            data.single(lambda x: x >= 4)

    def test_single_with_more_than_one_element(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.single()
        assert data.single(lambda x: x % 2 == 0) == 2
        with pytest.raises(Exception):
            data.single(lambda x: x % 2 != 0)
        with pytest.raises(Exception):
            data.single(lambda x: x >= 4)

    def test_count_with_non_empty(self):
        data = linq.range(1, 3)
        assert data.count(lambda x: x >= 2) == 2
        assert data.count() == 3

    def test_count_with_empty(self):
        assert linq.empty().count(lambda x: True) == 0
        assert linq.empty().count() == 0

    def test_contains_with_default_comp(self):
        data = linq.range(1, 3)
        assert data.contains(2) is True
        assert data.contains(4) is False

    def test_contains_with_custom_comp(self):
        data = linq.asEnumerable(["aa", "bb", "cc"])
        assert data.contains("cd", lambda x, y: x[0] == y[0]) is True
        assert data.contains("cd", lambda x, y: x[1] == y[1]) is False

    def test_contains_with_empty_sequence(self):
        data = linq.empty()
        assert data.contains(1) is False
        assert data.contains(1, lambda x, y: True) is False
        assert data.contains() is False

    def test_elementAtOrDefault_type_and_range(self):
        data = linq.range(1, 3)
        arrayData = linq.asEnumerable([1, 2, 3])
        for obj in (linq.empty(), data):
            with pytest.raises(Exception):
                obj.elementAtOrDefault("abc")
            with pytest.raises(Exception):
                obj.elementAtOrDefault()
        assert data.elementAtOrDefault(1) == 2
        assert arrayData.elementAtOrDefault(1) == 2
        assert data.elementAtOrDefault(-1) is None
        assert data.elementAtOrDefault(3) is None
        assert arrayData.elementAtOrDefault(-1) is None
        assert arrayData.elementAtOrDefault(3) is None

    def test_elementAt_type_and_range(self):
        data = linq.range(1, 3)
        arrayData = linq.asEnumerable([1, 2, 3])
        for obj in (linq.empty(), data):
            with pytest.raises(Exception):
                obj.elementAt("abc")
            with pytest.raises(Exception):
                obj.elementAt()
        assert data.elementAt(1) == 2
        assert arrayData.elementAt(1) == 2
        with pytest.raises(Exception):
            data.elementAt(-1)
        with pytest.raises(Exception):
            data.elementAt(3)
        with pytest.raises(Exception):
            arrayData.elementAt(-1)
        with pytest.raises(Exception):
            arrayData.elementAt(3)

    def test_firstOrDefault(self):
        data = linq.range(1, 3)
        assert data.firstOrDefault() == 1
        assert data.firstOrDefault(lambda x: x >= 2) == 2
        assert data.firstOrDefault(lambda x: x >= 4) is None
        data2 = linq.empty()
        assert data2.firstOrDefault() is None
        assert data2.firstOrDefault(lambda x: True) is None

    def test_first(self):
        data = linq.range(1, 3)
        assert data.first() == 1
        assert data.first(lambda x: x >= 2) == 2
        with pytest.raises(Exception):
            data.first(lambda x: x >= 4)
        data2 = linq.empty()
        with pytest.raises(Exception):
            data2.first()
        with pytest.raises(Exception):
            data2.first(lambda x: True)

    def test_lastOrDefault(self):
        data = linq.range(1, 3)
        arrayData = linq.asEnumerable([1, 2, 3])
        assert data.lastOrDefault() == 3
        assert arrayData.lastOrDefault() == 3
        assert data.lastOrDefault(lambda x: x <= 2) == 2
        assert arrayData.lastOrDefault(lambda x: x <= 2) == 2
        assert data.lastOrDefault(lambda x: x >= 4) is None
        assert arrayData.lastOrDefault(lambda x: x >= 4) is None
        data2 = linq.empty()
        arrayData2 = linq.asEnumerable([])
        assert data2.lastOrDefault() is None
        assert data2.lastOrDefault(lambda x: True) is None
        assert arrayData2.lastOrDefault() is None
        assert arrayData2.lastOrDefault(lambda x: True) is None

    def test_last(self):
        data = linq.range(1, 3)
        arrayData = linq.asEnumerable([1, 2, 3])
        assert data.last() == 3
        assert arrayData.last() == 3
        assert data.last(lambda x: x <= 2) == 2
        assert arrayData.last(lambda x: x <= 2) == 2
        with pytest.raises(Exception):
            data.last(lambda x: x >= 4)
        with pytest.raises(Exception):
            arrayData.last(lambda x: x >= 4)
        data2 = linq.empty()
        arrayData2 = linq.asEnumerable([])
        with pytest.raises(Exception):
            data2.last()
        with pytest.raises(Exception):
            data2.last(lambda x: True)
        with pytest.raises(Exception):
            arrayData2.last()
        with pytest.raises(Exception):
            arrayData2.last(lambda x: True)

    def test_defaultIfEmpty(self):
        assert linq.empty().defaultIfEmpty(1).toArray() == [1]
        assert len(linq.empty().defaultIfEmpty().toArray()) == 0
        data = linq.range(1, 3)
        assert data.defaultIfEmpty() is data

    def test_sequenceEqual(self):
        seq1 = linq.range(1, 3)
        seq2 = linq.range(1, 3)
        assert seq1.sequenceEqual(seq2) is True
        seq2 = linq.range(2, 3)
        assert seq1.sequenceEqual(seq2) is False
        seq2 = linq.range(1, 4)
        assert seq1.sequenceEqual(seq2) is False

    def test_min(self):
        data = linq.range(1, 3)
        assert data.min() == 1
        assert data.min(lambda x: -x) == -3
        data = linq.empty()
        assert data.min() is None
        assert data.min(lambda x: -x) is None

    def test_max(self):
        data = linq.range(1, 3)
        assert data.max() == 3
        assert data.max(lambda x: -x) == -1
        data = linq.empty()
        assert data.max() is None
        assert data.max(lambda x: -x) is None

    def test_sum(self):
        data = linq.repeat(1, 3)
        assert data.sum() == 3
        assert data.sum(lambda x: -x) == -3
        data = linq.empty()
        assert data.sum() == 0
        assert data.sum(lambda x: -x) == 0

    def test_average(self):
        data = linq.repeat(1, 3)
        assert data.average() == 1
        assert data.average(lambda x: -x) == -1
        data = linq.empty()
        assert data.average() == 0
        assert data.average(lambda x: -x) == 0