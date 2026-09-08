import pytest

class LineSegment:
    def __init__(self, *indexes):
        self.indexes = list(indexes)

    def get_start_idx(self):
        return self.indexes[0]

    def write_to_parcel(self, parcel, flags):
        parcel.data = list(self.indexes)

    def describe_contents(self):
        return 0

    class Creator:
        @staticmethod
        def create_from_parcel(parcel):
            return LineSegment(*parcel.data)
        @staticmethod
        def new_array(size):
            return [None] * size

    CREATOR = Creator()

class Parcel:
    def __init__(self):
        self.data = []
        self._position = 0
    @staticmethod
    def obtain():
        return Parcel()
    def set_data_position(self, pos):
        self._position = pos
    def recycle(self):
        pass

def test_constructor_and_get_start_idx_public():
    seg = LineSegment(10, 20, 30)
    assert seg.indexes == [10, 20, 30]
    assert seg.get_start_idx() == 10

def test_parcelable_write_and_read_public():
    seg = LineSegment(7, 8, 9)
    parcel = Parcel.obtain()
    seg.write_to_parcel(parcel, 0)
    parcel.set_data_position(0)

    created = LineSegment.CREATOR.create_from_parcel(parcel)
    assert created.indexes == [7, 8, 9]

    array = LineSegment.CREATOR.new_array(3)
    assert len(array) == 3

    parcel.recycle()

def test_describe_contents_public():
    seg = LineSegment(4, 8)
    assert seg.describe_contents() == 0