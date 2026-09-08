import pytest
import msgpack
from collections import namedtuple

def test_vector_pack_unpack():
    v = [1, 2, 3, 4, 5]
    packed = msgpack.packb(v)
    v2 = msgpack.unpackb(packed, raw=False)
    assert v == v2

def test_multi_pack_unpack():
    data1 = 10
    data2 = "monado"
    data3 = [1, 2, 3]

    packed = b''
    packed += msgpack.packb(data1)
    packed += msgpack.packb(data2)
    packed += msgpack.packb(data3)
    # Iterate over messages using unpacker
    cnt = 0
    offset = 0
    unpacker = msgpack.Unpacker(raw=False)
    unpacker.feed(packed)
    for obj in unpacker:
        cnt += 1
    assert cnt == 3

def test_object_class():
    # Simulate Book with id, title, tags and msgpack
    Book = namedtuple('Book', ['id', 'title', 'tags'])
    book1 = Book(42, "gtest", {"x", "y"})
    # Convert set to list for JSON/msgpack compatibility
    book1_dict = {"id": book1.id, "title": book1.title, "tags": sorted(list(book1.tags))}
    packed = msgpack.packb(book1_dict)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked['id'] == 42
    assert unpacked['title'] == "gtest"
    assert set(unpacked['tags']) == {"x", "y"}
    assert len(unpacked['tags']) == 2

def test_unpack_empty_throws():
    empty_txt = b""
    with pytest.raises(Exception):
        msgpack.unpackb(empty_txt, raw=False)