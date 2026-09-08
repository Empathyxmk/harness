from collections import namedtuple
import records
from pytest import raises

OtherRecord = namedtuple('OtherRecord', 'val')

def check_val(i, row):
    assert row.val == i

class TestPublicRecordCollection:
    def test_iter(self):
        rows = records.RecordCollection(OtherRecord(i * 2) for i in range(8))
        for i, row in enumerate(rows):
            check_val(i * 2, row)

    def test_next(self):
        rows = records.RecordCollection(OtherRecord(i * 2) for i in range(8))
        for i in range(8):
            check_val(i * 2, next(rows))

    def test_iter_and_next(self):
        rows = records.RecordCollection(OtherRecord(i * 2) for i in range(8))
        i = enumerate(iter(rows))
        check_val(*next(i))
        next(rows)
        check_val(*next(i))

    def test_multiple_iter(self):
        rows = records.RecordCollection(OtherRecord(i * 2) for i in range(8))
        i = enumerate(iter(rows))
        j = enumerate(iter(rows))

        check_val(*next(i))
        check_val(*next(j))
        check_val(*next(j))
        check_val(*next(i))

    def test_slice_iter(self):
        rows = records.RecordCollection(OtherRecord(i * 2) for i in range(8))
        for i, row in enumerate(rows[:3]):
            check_val(i * 2, row)
        for i, row in enumerate(rows):
            check_val(i * 2, row)
        assert len(rows) == 8

    def test_all_returns_a_list_of_records(self):
        rows = records.RecordCollection(OtherRecord(i * 2) for i in range(2))
        assert rows.all() == [OtherRecord(0), OtherRecord(2)]

    def test_first_returns_a_single_record(self):
        rows = records.RecordCollection(OtherRecord(i * 2 + 100) for i in range(1))
        assert rows.first() == OtherRecord(100)

    def test_first_defaults_to_None(self):
        rows = records.RecordCollection(iter([]))
        assert rows.first() is None

    def test_first_default_is_overridable(self):
        rows = records.RecordCollection(iter([]))
        assert rows.first('Hamster') == 'Hamster'

    def test_first_raises_default_if_its_an_exception_subclass(self):
        rows = records.RecordCollection(iter([]))
        class Hamster(Exception): pass
        raises(Hamster, rows.first, Hamster)

    def test_first_raises_default_if_its_an_exception_instance(self):
        rows = records.RecordCollection(iter([]))
        class Hamster(Exception): pass
        raises(Hamster, rows.first, Hamster('dwarf'))

    def test_one_returns_a_single_record(self):
        rows = records.RecordCollection(OtherRecord(5) for i in range(1))
        assert rows.one() == OtherRecord(5)

    def test_one_defaults_to_None(self):
        rows = records.RecordCollection(iter([]))
        assert rows.one() is None

    def test_one_default_is_overridable(self):
        rows = records.RecordCollection(iter([]))
        assert rows.one('Rabbit') == 'Rabbit'

    def test_one_raises_when_more_than_one(self):
        rows = records.RecordCollection(OtherRecord(i + 3) for i in range(4))
        raises(ValueError, rows.one)

    def test_one_raises_default_if_its_an_exception_subclass(self):
        rows = records.RecordCollection(iter([]))
        class Rabbit(Exception): pass
        raises(Rabbit, rows.one, Rabbit)

    def test_one_raises_default_if_its_an_exception_instance(self):
        rows = records.RecordCollection(iter([]))
        class Rabbit(Exception): pass
        raises(Rabbit, rows.one, Rabbit('lop'))

    def test_scalar_returns_a_single_record(self):
        rows = records.RecordCollection(OtherRecord(24) for i in range(1))
        assert rows.scalar() == 24

    def test_scalar_defaults_to_None(self):
        rows = records.RecordCollection(iter([]))
        assert rows.scalar() is None

    def test_scalar_default_is_overridable(self):
        rows = records.RecordCollection(iter([]))
        assert rows.scalar('Catnip') == 'Catnip'

    def test_scalar_raises_when_more_than_one(self):
        rows = records.RecordCollection(OtherRecord(i * 3) for i in range(4))
        raises(ValueError, rows.scalar)

class TestPublicRecord:
    def test_record_dir(self):
        keys, values = ['uid', 'title', 'desc'], [10, 'some', 'd']
        record = records.Record(keys, values)
        _dir = dir(record)
        for key in keys:
            assert key in _dir
        for key in dir(object):
            assert key in _dir

    def test_record_duplicate_column(self):
        keys, values = ['uid', 'title', 'desc', 'desc'], [10, 'some', 'd', 'd2']
        record = records.Record(keys, values)
        from pytest import raises
        with raises(KeyError):
            record['desc']