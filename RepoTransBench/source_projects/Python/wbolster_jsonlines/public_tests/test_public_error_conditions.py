import pytest
import jsonlines

def test_public_reader_wrong_mode(tmp_path):
    # Opening in binary mode will decode bytes to utf-8 and then try to parse as JSON
    # Let's write non-JSON valid content to ensure InvalidLineError is triggered as expected
    file_path = tmp_path / "pub_not_existing2.txt"
    file_path.write_bytes(b"notjson\nsurely-not-json-either\n")
    with open(file_path, "rb") as f:
        reader = jsonlines.Reader(f)
        # Should raise InvalidLineError because neither line is valid JSON
        with pytest.raises(jsonlines.jsonlines.InvalidLineError):
            list(reader)

def test_public_writer_wrong_mode(tmp_path):
    # Writer should function but writing to a binary file will produce bytes, not str.
    # Actually, writing to a binary file will succeed, but the output will be bytes!
    # We check that bytes are written (but NOT that it raises TypeError)
    file_path = tmp_path / "pub_myfile_binary.txt"
    with open(file_path, "wb") as f:
        writer = jsonlines.Writer(f)
        writer.write({"write": "to-binary"})
        writer.close()
    # Now read back and check what was written
    with open(file_path, "rb") as f:
        raw = f.read()
    # It should be a JSON string line ending with \n (all bytes)
    assert b'"write": "to-binary"' in raw
    assert raw.endswith(b"\n")

def test_public_reader_iterable(tmp_path):
    class CustomIterable:
        def __iter__(self):
            return iter([
                '{"thing_a": 42}\n', '{"thing_b": [5, 7, 9]}\n'
            ])
    result = list(jsonlines.Reader(CustomIterable()))
    assert result == [{"thing_a": 42}, {"thing_b": [5, 7, 9]}]

def test_public_writer_non_dict(tmp_path):
    # Write a string and a float value
    file_path = tmp_path / "pub_test2.jsonl"
    with open(file_path, "w", encoding="utf-8") as f:
        writer = jsonlines.Writer(f)
        writer.write("something completely else")
        writer.write(3.1415)
        writer.close()
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    assert lines[0].strip() == '"something completely else"'
    assert lines[1].strip() == "3.1415"

def test_public_reader_writer_repr(tmp_path):
    file_path = tmp_path / "pub_file2.jsonl"
    with open(file_path, "w", encoding="utf-8") as f:
        w = jsonlines.Writer(f)
        # The repr shows its class and path
        r = repr(w)
        assert r.startswith("<jsonlines.Writer ")
    with open(file_path, "r", encoding="utf-8") as f:
        r = jsonlines.Reader(f)
        s = repr(r)
        assert s.startswith("<jsonlines.Reader ")

def test_public_reader_context_manager(tmp_path):
    file_path = tmp_path / "pub_lines2.jsonl"
    file_path.write_text('{"fooX_pub": 841}\n{"barX_pub": 1881}\n')
    with open(file_path, encoding="utf-8") as f:
        with jsonlines.Reader(f) as reader:
            out = list(reader)
    assert out == [{"fooX_pub": 841}, {"barX_pub": 1881}]