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

def test_default_dumps_not_implemented():
    import jsonlines.jsonlines as jlmod
    with pytest.raises(NotImplementedError):
        jlmod.default_dumps(None)

def test_invalid_line_error_properties():
    err = InvalidLineError("Bad", "bad json line", 3)
    assert isinstance(err, ValueError)
    assert isinstance(err, Error)
    assert err.line == "bad json line"
    assert err.lineno == 3
    assert "Bad" in str(err)
    err2 = InvalidLineError("Test", "line\n", 5)
    assert err2.line == "line"

def test_readerwriterbase_close_called_multiple_times():
    base = jsonlines.jsonlines.ReaderWriterBase()
    base.close()
    base.close()

def test_readerwriterbase_eq():
    base1 = jsonlines.jsonlines.ReaderWriterBase()
    base2 = jsonlines.jsonlines.ReaderWriterBase()
    assert base1 == base2

def test_writer_write_obj_types(tmp_path):
    path = tmp_path / "test.jsonl"
    with open(path, mode='w+', encoding='utf-8') as f:
        with Writer(f) as writer:
            writer.write({"k": 1})
            # flush to ensure written for reading next lines
            f.flush()
            f.seek(0)
            r = Reader(f)
            items = list(r)
            r.close()
            assert items == [{"k": 1}]

def test_writer_writes_supported_types(tmp_path):
    path = tmp_path / "test2.jsonl"
    data = [
        {"a": 1},
        [1, 2, 3],
        1,
        2.5,
        True,
        "hello"
    ]
    with open(path, 'w+', encoding='utf-8') as f:
        with Writer(f) as writer:
            for item in data:
                writer.write(item)
    with open(path, 'r', encoding='utf-8') as f:
        with Reader(f) as reader:
            got = list(reader)
            assert got == data

def test_writer_write_unsupported_type(tmp_path):
    path = tmp_path / "test3.jsonl"
    class C:
        pass
    with open(path, "w", encoding="utf-8") as f:
        with Writer(f) as writer:
            with pytest.raises(TypeError):
                writer.write(C())

def test_writer_close(tmp_path):
    path = tmp_path / "test_flush.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        with Writer(f) as writer:
            writer.write({"a": 1})
        # Writer handles flush/close via context manager

def test_reader_valid_and_eof(tmp_path):
    text = '{"a":1}\n{"b":2}\n'
    file_path = tmp_path / "test_read.jsonl"
    file_path.write_text(text)
    with open(str(file_path), "r", encoding="utf-8") as f:
        with Reader(f) as r:
            a = r.read()
            assert a == {"a": 1}
            b = r.read()
            assert b == {"b": 2}
            with pytest.raises(EOFError):
                r.read()
        # Extra close to test idempotency:
        r.close()
        r.close()

def test_reader_invalid_line(tmp_path):
    file_path = tmp_path / "test_inv.jsonl"
    # orjson requires valid UTF-8 and JSON; 'notjson' is not valid JSON.
    file_path.write_text('{"a":1}\nnotjson\n')
    with open(str(file_path), "r", encoding="utf-8") as f:
        with Reader(f) as r:
            a = r.read()
            assert a == {"a": 1}
            with pytest.raises(InvalidLineError) as exc:
                r.read()
            assert "notjson" in str(exc.value) or "invalid json" in str(exc.value)

def test_reader_skip_initial_char(tmp_path):
    file_path = tmp_path / "test_skip.jsonl"
    bom = b'\xef\xbb\xbf'
    with open(file_path, "wb") as f:
        f.write(bom + b'{"x": 1}\n')
    with open(str(file_path), "rb") as f:
        with Reader(f) as r:
            v = r.read()
            assert v == {"x": 1}
            with pytest.raises(EOFError):
                r.read()

def test_writer_mode_bytes(tmp_path):
    path = tmp_path / "test_bytes.jsonl"
    with open(path, "wb+") as f:
        with Writer(f) as writer:
            writer.write({"k": 42})
    with open(path, "rb") as fb:
        with Reader(fb) as reader:
            v = reader.read()
            assert v == {"k": 42}
            with pytest.raises(EOFError):
                reader.read()

def test_open_function_modes(tmp_path):
    fpath = tmp_path / "openf.jsonl"
    with jsonlines.open(str(fpath), mode="w") as w:
        w.write({"value": 42})
    with jsonlines.open(str(fpath), mode="r") as r:
        assert r.read()["value"] == 42

def test_reader_writer_base_context_manager():
    b = jsonlines.jsonlines.ReaderWriterBase()
    b.__enter__()
    b.close()
    b.__exit__(None, None, None)