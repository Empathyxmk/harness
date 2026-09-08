import codecs
import io
import json
import pytest

import jsonlines

ALT_SAMPLE_BYTES = b'{"m": 10}\n{"n": 20}\n'
ALT_SAMPLE_TEXT = ALT_SAMPLE_BYTES.decode("utf-8")

def is_json_decode_error_public(exc: object) -> bool:
    if type(exc).__module__ == "ujson":
        import ujson
        return isinstance(exc, ujson.JSONDecodeError)
    else:
        return isinstance(exc, json.JSONDecodeError)

def test_public_reader():
    fp = io.BytesIO(ALT_SAMPLE_BYTES)
    with jsonlines.Reader(fp) as reader:
        it = iter(reader)
        assert next(it) == {"m": 10}
        assert next(it) == {"n": 20}
        with pytest.raises(StopIteration):
            next(it)
        with pytest.raises(EOFError):
            reader.read()

def test_public_reading_from_iterable():
    with jsonlines.Reader(["5", b'{"x":1}']) as reader:
        assert list(reader) == [5, {"x":1}]
    assert "wrapping <list at " in repr(reader)

def test_public_reader_rfc7464_text_sequences():
    fp = io.BytesIO(b'\x1e"A"\x0a\x1e"B"\x0a')
    with jsonlines.Reader(fp) as reader:
        assert list(reader) == ["A", "B"]

def test_public_reader_utf8_bom_bytes():
    chunks = [
        codecs.BOM_UTF8,
        b"3\n",
        codecs.BOM_UTF8,
        b"4\n",
    ]
    fp = io.BytesIO(b"".join(chunks))
    with jsonlines.Reader(fp) as reader:
        assert list(reader) == [3, 4]

def test_public_reader_utf8_bom_text():
    chunks = [
        "7\n",
        codecs.BOM_UTF8.decode(),
        "8\n",
    ]
    fp = io.StringIO("".join(chunks))
    with jsonlines.Reader(fp) as reader:
        assert list(reader) == [7, 8]

def test_public_reader_utf8_bom_bombombom():
    reader = jsonlines.Reader([codecs.BOM_UTF8.decode() * 2 + "17\n"])
    with pytest.raises(jsonlines.InvalidLineError) as excinfo:
        reader.read()
    exc = excinfo.value
    assert "invalid json" in str(exc)
    assert is_json_decode_error_public(exc.__cause__)

def test_public_writer_text():
    fp = io.StringIO()
    with jsonlines.Writer(fp) as writer:
        writer.write({"alpha": 123})
        writer.write({"beta": 456})
    assert fp.getvalue() == '{"alpha": 123}\n{"beta": 456}\n'

def test_public_writer_binary():
    fp = io.BytesIO()
    with jsonlines.Writer(fp) as writer:
        writer.write_all([{"foo": 11}, {"bar": 22}])
    assert fp.getvalue() == b'{"foo": 11}\n{"bar": 22}\n'

def test_public_closing():
    reader = jsonlines.Reader([])
    reader.close()
    with pytest.raises(RuntimeError):
        reader.read()
    writer = jsonlines.Writer(io.BytesIO())
    writer.close()
    writer.close()
    with pytest.raises(RuntimeError):
        writer.write(987)

def test_public_invalid_lines():
    data = '[9, 11'
    with jsonlines.Reader(io.StringIO(data)) as reader:
        with pytest.raises(jsonlines.InvalidLineError) as excinfo:
            reader.read()
        exc = excinfo.value
        assert "invalid json" in str(exc)
        assert exc.line == data
        assert is_json_decode_error_public(exc.__cause__)

def test_public_skip_invalid():
    fp = io.StringIO("100\nbad\n200")
    reader = jsonlines.Reader(fp)
    it = reader.iter(skip_invalid=True)
    assert next(it) == 100
    assert next(it) == 200

def test_public_empty_strings_in_iterable():
    input = ["789", "", "321"]
    it = iter(jsonlines.Reader(input))
    assert next(it) == 789
    with pytest.raises(jsonlines.InvalidLineError):
        next(it)
    with pytest.raises(StopIteration):
        next(it)
    it = jsonlines.Reader(input).iter(skip_empty=True)
    assert list(it) == [789, 321]

def test_public_invalid_utf8():
    with jsonlines.Reader([b"\xfe\xfe"]) as reader:
        with pytest.raises(jsonlines.InvalidLineError) as excinfo:
            reader.read()
        assert "line is not valid utf-8" in str(excinfo.value)

def test_public_empty_lines():
    data_with_empty_line = b"55\n\n66\n"
    with jsonlines.Reader(io.BytesIO(data_with_empty_line)) as reader:
        assert reader.read()
        with pytest.raises(jsonlines.InvalidLineError):
            reader.read()
        assert reader.read() == 66
        with pytest.raises(EOFError):
            reader.read()
    with jsonlines.Reader(io.BytesIO(data_with_empty_line)) as reader:
        assert list(reader.iter(skip_empty=True)) == [55, 66]

def test_public_typed_reads():
    with jsonlines.Reader(io.StringIO('43\nfalse\n"bar"\n')) as reader:
        assert reader.read(type=int) == 43
        with pytest.raises(jsonlines.InvalidLineError) as excinfo:
            reader.read(type=int)
        exc = excinfo.value
        assert "does not match requested type" in str(exc)
        assert exc.line == "false"
        with pytest.raises(jsonlines.InvalidLineError) as excinfo:
            reader.read(type=float)
        exc = excinfo.value
        assert "does not match requested type" in str(exc)
        assert exc.line == '"bar"'

def test_public_typed_read_invalid_type():
    reader = jsonlines.Reader([])
    with pytest.raises(ValueError) as excinfo:
        reader.read(type="nope")
    exc = excinfo.value
    assert str(exc) == "invalid type specified"

def test_public_typed_iteration():
    fp = io.StringIO("13\n14\n")
    with jsonlines.Reader(fp) as reader:
        actual = list(reader.iter(type=int))
        assert actual == [13, 14]