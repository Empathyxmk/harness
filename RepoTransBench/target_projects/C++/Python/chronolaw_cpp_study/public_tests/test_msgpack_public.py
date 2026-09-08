import pytest
import msgpack

from collections import namedtuple

def test_public_case1():
    v = [9,8,7,6]
    packed = msgpack.packb(v)
    v2 = msgpack.unpackb(packed, raw=False)
    assert v == v2

def test_public_case2():
    data1 = 99
    data2 = "public_test"
    data3 = [10, 20]
    packed = b''
    packed += msgpack.packb(data1)
    packed += msgpack.packb(data2)
    packed += msgpack.packb(data3)
    unpacker = msgpack.Unpacker(raw=False)
    unpacker.feed(packed)
    received = []
    for obj in unpacker:
        received.append(obj)
    assert received[0] == 99
    assert received[1] == "public_test"
    assert received[2] == [10, 20]

def test_public_case3():
    # PublicBook: id, title, tags
    PublicBook = namedtuple("PublicBook", ["id", "title", "tags"])
    book1 = PublicBook(42, "The Art of C++", {"x", "y", "z"})
    # For msgpack serialization, use a dict and tag as a sorted list
    book1_dict = {"id": book1.id, "title": book1.title, "tags": sorted(list(book1.tags))}
    packed = msgpack.packb(book1_dict)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked["id"] == book1.id
    assert unpacked["title"] == book1.title
    assert set(unpacked["tags"]) == {"x", "y", "z"}
    assert len(unpacked["tags"]) == 3

def test_public_case4():
    txt = b"invalid data"
    with pytest.raises(Exception):
        msgpack.unpackb(txt, raw=False)