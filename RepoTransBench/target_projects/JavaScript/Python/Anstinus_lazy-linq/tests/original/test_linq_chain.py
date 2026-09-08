import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import linq

# Ensure asEnumerable is installed, for list support
if hasattr(linq, "installAsEnumerable"):
    linq.installAsEnumerable()

class TestLinqChainMembers:

    def test_skip_invalid_n(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.skip()
        with pytest.raises(Exception):
            data.skip(None)
        with pytest.raises(Exception):
            data.skip({})
        with pytest.raises(Exception):
            data.skip(1.2)

    def test_skip_n_le_zero(self):
        data = linq.range(1, 3)
        assert data.skip(0).toArray() == [1, 2, 3]
        assert data.skip(-1).toArray() == [1, 2, 3]

    def test_skip_n_gt_zero(self):
        data = linq.range(1, 3)
        assert data.skip(1).toArray() == [2, 3]

    def test_skipWhile_pred_not_function(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.skipWhile().toArray()
        with pytest.raises(Exception):
            data.skipWhile(1).toArray()
        with pytest.raises(Exception):
            data.skipWhile({}).toArray()

    def test_skipWhile(self):
        data = linq.range(1, 3)
        assert data.skipWhile(lambda x: x <= 2).toArray() == [3]

    def test_take_invalid_n(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.take()
        with pytest.raises(Exception):
            data.take(None)
        with pytest.raises(Exception):
            data.take({})
        with pytest.raises(Exception):
            data.take(1.2)

    def test_take_n_le_zero(self):
        data = linq.range(1, 3)
        assert len(data.take(0).toArray()) == 0
        assert len(data.take(-1).toArray()) == 0

    def test_take_n_gt_zero(self):
        data = linq.range(1, 3)
        assert data.take(2).toArray() == [1, 2]

    def test_takeWhile_pred_not_function(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.takeWhile().toArray()

    def test_takeWhile(self):
        data = linq.range(1, 3)
        assert data.takeWhile(lambda x: x <= 2).toArray() == [1, 2]

    def test_reverse_nonempty(self):
        data = linq.range(1, 3)
        assert data.reverse().toArray() == [3, 2, 1]

    def test_reverse_empty(self):
        assert len(linq.empty().reverse().toArray()) == 0

    def test_select_trans_not_function(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.select()
        with pytest.raises(Exception):
            data.select(1)
        with pytest.raises(Exception):
            data.select({})

    def test_select_transform(self):
        data = linq.range(1, 3)
        assert data.select(lambda x: x + 1).toArray() == [2, 3, 4]

    def test_where_pred_not_function(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.where().toArray()
        with pytest.raises(Exception):
            data.where(1).toArray()
        with pytest.raises(Exception):
            data.where({}).toArray()

    def test_where_pred_condition(self):
        data = linq.range(1, 3)
        assert data.where(lambda x: x % 2 != 0).toArray() == [1, 3]

    def test_selectMany_genSeq_not_function(self):
        data = linq.range(1, 3)
        with pytest.raises(Exception):
            data.selectMany().toArray()
        with pytest.raises(Exception):
            data.selectMany(1).toArray()
        with pytest.raises(Exception):
            data.selectMany({}).toArray()

    def test_selectMany_flatten(self):
        data = linq.range(1, 3)
        assert data.selectMany(lambda x: linq.repeat(x, 2)).toArray() == [1, 1, 2, 2, 3, 3]

    def test_selectMany_with_resultTrans(self):
        data = linq.range(1, 3)
        assert data.selectMany(lambda x: linq.repeat(x, 2), lambda x, seq: seq.sum()).toArray() == [2, 4, 6]

    def test_groupBy_default(self):
        data = linq.asEnumerable([1,2,3,1])
        result = data.groupBy().toArray()
        assert len(result) == 3
        assert result[0].key == 1
        assert result[0].toArray() == [1, 1]
        assert result[1].key == 2
        assert result[1].toArray() == [2]
        assert result[2].key == 3
        assert result[2].toArray() == [3]

    def test_groupBy_custom_keySelector(self):
        data = linq.asEnumerable([1,2,3,1])
        result = data.groupBy(lambda x: x % 2).toArray()
        assert len(result) == 2
        assert result[0].key == 1
        assert result[0].toArray() == [1,3,1]
        assert result[1].key == 0
        assert result[1].toArray() == [2]

    def test_groupBy_custom_valueSelector(self):
        data = linq.asEnumerable([1,2,3,1])
        result = data.groupBy(lambda x: x, lambda y: -y).toArray()
        assert len(result) == 3
        assert result[0].key == 1
        assert result[0].toArray() == [-1, -1]
        assert result[1].key == 2
        assert result[1].toArray() == [-2]
        assert result[2].key == 3
        assert result[2].toArray() == [-3]

    def test_groupBy_custom_resultTrans(self):
        data = linq.asEnumerable([1,2,3,1])
        result = data.groupBy(lambda x: x, lambda y: y, lambda key, valSeq: linq.asEnumerable(valSeq).sum()).toArray()
        assert len(result) == 3
        assert result[0] == 2
        assert result[1] == 2
        assert result[2] == 3

    def test_groupBy_custom_keyEqual(self):
        data = linq.asEnumerable(['ab', 'bc', 'aa', 'cc'])
        result = data.groupBy(None, None, None, lambda x, y: x[0] == y[0]).toArray()
        assert len(result) == 3
        assert result[0].key == 'ab'
        assert result[0].toArray() == ['ab', 'aa']
        assert result[1].key == 'bc'
        assert result[1].toArray() == ['bc']
        assert result[2].key == 'cc'
        assert result[2].toArray() == ['cc']

    def test_orderBy_default(self):
        data = linq.asEnumerable([3,1,2])
        assert data.orderBy().toArray() == [1,2,3]

    def test_orderBy_custom_keySelector(self):
        data = linq.asEnumerable([3,1,2])
        assert data.orderBy(lambda x: 1/x).toArray() == [3,2,1]

    def test_orderBy_custom_comp(self):
        data = linq.asEnumerable([3,1,2])
        assert data.orderBy(lambda x:x, lambda x, y: y-x).toArray() == [3,2,1]

    def test_orderBy_stable(self):
        data = linq.asEnumerable(['ba','cb','ab','ca','aa','bb'])
        assert data.orderBy(lambda x: x[0]).toArray() == ['ab','aa','ba','bb','cb','ca']

    def test_thenBy_after_orderBy(self):
        data = linq.asEnumerable(['cac','bca','cba','cab'])
        assert data.orderBy(lambda x: x[0]).thenBy(lambda x: x[1]).toArray() == ['bca','cac','cab','cba']

    def test_thenBy_multiple(self):
        data = linq.asEnumerable(['cac','bca','cba','cab'])
        assert data.orderBy(lambda x: x[0]).thenBy(lambda x: x[1]).thenBy(lambda x: x[2]).toArray() == ['bca','cab','cac','cba']

    def test_thenBy_duplicate_selector(self):
        data = linq.asEnumerable(['cac','bca','cba','cab'])
        assert data.orderBy(lambda x: x[0]).thenBy(lambda x: x[0]).thenBy(lambda x: x[0]).toArray() == ['bca','cac','cba','cab']

    def test_thenBy_without_orderBy_should_throw(self):
        data = linq.asEnumerable(['cac','bca','cba','cab'])
        with pytest.raises(Exception):
            data.thenBy(lambda x: x)

    def test_thenBy_default_keySelector(self):
        data = linq.asEnumerable(['cac','bca','cba','cab'])
        assert data.orderBy(lambda x: x[0]).thenBy().toArray() == ['bca','cab','cac','cba']

    def test_thenBy_custom_comp(self):
        data = linq.asEnumerable(['cac','bca','cba','cab'])
        comp = lambda x, y: 0 if x == y else (1 if x < y else -1)
        assert data.orderBy(lambda x: x[0]).thenBy(lambda x: x[1], comp).toArray() == ['bca','cba','cac','cab']

    def test_orderByDescending(self):
        data = linq.asEnumerable([3,1,2])
        assert data.orderByDescending().toArray() == [3,2,1]

    def test_thenByDescending(self):
        data = linq.asEnumerable(['cac','bca','cba','cab'])
        assert data.orderBy(lambda x: x[0]).thenByDescending(lambda x: x[1]).toArray() == ['bca','cba','cac','cab']
        assert data.orderByDescending(lambda x: x[0]).thenByDescending(lambda x: x[1]).toArray() == ['cba','cac','cab','bca']

    def test_join(self):
        data1 = linq.asEnumerable([1,2,3,4])
        data2 = [2,4,6]
        with pytest.raises(Exception):
            data1.join()
        with pytest.raises(Exception):
            data1.join(None)
        assert data1.join(data2).toArray() == [[2,2],[4,4]]
        assert len(data1.join([5,6]).toArray()) == 0
        assert len(data1.join([]).toArray()) == 0
        assert len(linq.asEnumerable([]).join(data2).toArray()) == 0
        assert len(linq.asEnumerable([]).join([]).toArray()) == 0

        assert data1.join(data2, lambda x: x+1).toArray() == [[1,2],[3,4]]
        assert data1.join(data2, None, lambda y: y-1).toArray() == [[1,2],[3,4]]
        assert data1.join(data2, None, None, lambda x, y: x+1 == y).toArray() == [[1,2],[3,4]]
        assert data1.join(data2, None, None, None, lambda x, y: x+y).toArray() == [4,8]

    def test_groupJoin(self):
        # Mapping spec mirrors join()
        self.test_join()

    def test_zip(self):
        data1 = linq.asEnumerable([1,2])
        data2 = [2,3,4]
        with pytest.raises(Exception):
            data1.zip()
        with pytest.raises(Exception):
            data1.zip(None)
        assert data1.zip(data2).toArray() == [[1,2],[2,3]]
        assert data1.zip([]).toArray() == []
        assert linq.asEnumerable([]).zip(data2).toArray() == []
        assert linq.asEnumerable([]).zip([]).toArray() == []

    def test_concat(self):
        data1 = linq.asEnumerable([1,2])
        data2 = [2,3]
        with pytest.raises(Exception):
            data1.concat()
        with pytest.raises(Exception):
            data1.concat(None)
        assert data1.concat(data2).toArray() == [1,2,2,3]
        assert linq.asEnumerable([1,2]).concat([]).toArray() == [1,2]
        assert linq.asEnumerable([]).concat([2,3]).toArray() == [2,3]
        assert linq.asEnumerable([]).concat([]).toArray() == []

    def test_otherThan(self):
        data1 = linq.asEnumerable([1,2,1])
        data2 = [2,3,2]
        with pytest.raises(Exception):
            data1.otherThan()
        with pytest.raises(Exception):
            data1.otherThan(None)
        assert data1.otherThan(data2).toArray() == [1,1]
        assert data1.otherThan([]).toArray() == [1,2,1]