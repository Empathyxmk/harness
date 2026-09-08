import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import linq

class TestLinqLibHelper:
    def test_range_should_generate_incremental_sequence(self):
        assert linq.range(1,3).toArray() == [1,2,3]

    def test_range_with_count_0_should_generate_empty(self):
        assert len(linq.range(1,0).toArray()) == 0

    def test_range_with_count_lt_0_should_generate_empty(self):
        assert len(linq.range(1,-1).toArray()) == 0

    def test_range_toArray_again_should_produce_same_result(self):
        data = linq.range(1,3)
        assert data.toArray() == [1,2,3]
        assert data.toArray() == [1,2,3]

    def test_repeat_should_generate_identical_sequence(self):
        assert linq.repeat(1,3).toArray() == [1,1,1]

    def test_repeat_with_count_0_should_generate_empty(self):
        assert len(linq.repeat(1,0).toArray()) == 0

    def test_repeat_with_count_lt_0_should_generate_empty(self):
        assert len(linq.repeat(1,-1).toArray()) == 0

    def test_repeat_toArray_again_should_produce_same_result(self):
        data = linq.repeat(1,3)
        assert data.toArray() == [1,1,1]
        assert data.toArray() == [1,1,1]

    def test_empty_should_be_empty(self):
        assert len(linq.empty().toArray()) == 0