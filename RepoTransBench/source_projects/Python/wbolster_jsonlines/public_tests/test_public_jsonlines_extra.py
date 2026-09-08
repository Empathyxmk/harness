import io
import os
import pytest

import jsonlines
from jsonlines import (
    Error,
    InvalidLineError,
    Reader,
    Writer,
)

def test_public_default_dumps_not_implemented():
    import jsonlines.jsonlines as jlmod
    with pytest.raises(NotImplementedError):
        jlmod.default_dumps(123)

def test_public_invalid_line_error_properties():
    err = InvalidLineError("Oops", "another bad json", 7)
    assert isinstance(err, ValueError)
    assert isinstance(err, Error)
    assert err.line == "another bad json"
    assert err.lineno == 7
    assert "Oops" in str(err)
    err2 = InvalidLineError("Msg", "lineagain\n", 4)
    assert err2.line == "lineagain"

def test_public_readerwriterbase_close_multiple():
    base = jsonlines.jsonlines.ReaderWriterBase()
    base.close()
    base.close()

def test_public_readerwriterbase_eq():
    base1 = jsonlines.jsonlines.ReaderWriterBase()
    base2 = jsonlines.jsonlines.ReaderWriterBase()
    assert base1 == base2

def test_public_writer_write_obj_types(tmp_path):
    path = tmp_path / "public_test.jsonl"
    with open(path, mode='w+', encoding='utf-8') as f:
        with Writer(f) as writer:
            writer.write({"xyz": 15})
            f.flush()
            f.seek(0)
            r = Reader(f)
            items = list(r)
            r.close()
            assert items == [{"xyz": 15}]

def test_public_writer_writes_supported_types(tmp_path):
    path = tmp_path / "public_test2.jsonl"
    data = [
        {"foo": 9},
        [5, 4],
        7,
        0.1,
        False,
        "world"
    ]
    with open(path, 'w+', encoding='utf-8') as f:
        with Writer(f) as writer:
            for item in data:
                writer.write(item)
    with open(path, 'r', encoding='utf-8') as f:
        with Reader(f) as reader:
            got = list(reader)
            assert got == data

def test_public_writer_write_unsupported_type(tmp_path):
    path = tmp_path / "public_test3.jsonl"
    class D:
        pass
    with open(path, "w", encoding="utf-8") as f:
        with Writer(f) as writer:
            with pytest.raises(TypeError):
                writer.write(D())

def test_public_writer_close(tmp_path):
    path = tmp_path / "public_flush.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        with Writer(f) as writer:
            writer.write({"bar": 10})

def test_public_reader_valid_and_eof(tmp_path):
    text = '{"x":42}\n{"y":77}\n'
    file_path = tmp_path / "public_read.jsonl"
    file_path.write_text(text)
    with open(str(file_path), "r", encoding="utf-8") as f:
        with Reader(f) as r:
            a = r.read()
            assert a == {"x": 42}
            b = r.read()
            assert b == {"y": 77}
            with pytest.raises(EOFError):
                r.read()
        r.close()
        r.close()

def test_public_reader_invalid_line(tmp_path):
    file_path = tmp_path / "public_inv.jsonl"
    file_path.write_text('{"key":5}\nNOTJSON\n')
    with open(str(file_path), "r", encoding="utf-8") as f:
        with Reader(f) as r:
            a = r.read()
            assert a == {"key": 5}
            with pytest.raises(InvalidLineError) as exc:
                r.read()
            assert "NOTJSON" in str(exc.value) or "invalid json" in str(exc.value)

def test_public_reader_skip_initial_char(tmp_path):
    file_path = tmp_path / "public_skip.jsonl"
    bom = b'\xef\xbb\xbf'
    with open(file_path, "wb") as f:
        f.write(bom + b'{"z": 123}\n')
    with open(str(file_path), "rb") as f:
        with Reader(f) as r:
            v = r.read()
            assert v == {"z": 123}
            with pytest.raises(EOFError):
                r.read()

def test_public_writer_mode_bytes(tmp_path):
    path = tmp_path / "public_bytes.jsonl"
    with open(path, "wb+") as f:
        with Writer(f) as writer:
            writer.write({"val": 108})
    with open(path, "rb") as fb:
        with Reader(fb) as reader:
            v = reader.read()
            assert v == {"val": 108}
            with pytest.raises(EOFError):
                reader.read()

def test_public_open_function_modes(tmp_path):
    fpath = tmp_path / "public_openf.jsonl"
    with jsonlines.open(str(fpath), mode="w") as w:
        w.write({"value": 73})
    with jsonlines.open(str(fpath), mode="r") as r:
        assert r.read()["value"] == 73

def test_public_reader_writer_base_context_manager():
    b = jsonlines.jsonlines.ReaderWriterBase()
    b.__enter__()
    b.close()
    b.__exit__(None, None, None)