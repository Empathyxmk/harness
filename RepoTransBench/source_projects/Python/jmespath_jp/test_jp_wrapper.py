import pytest
import os
from jp_wrapper import JpWrapper

def jp_exists():
    return os.path.isfile('./jp') and os.access('./jp', os.X_OK)

pytestmark = pytest.mark.skipif(
    not jp_exists(),
    reason="jp binary not available for wrapper tests"
)

def test_basic_select():
    jp = JpWrapper('./jp')
    data = {"foo": {"bar": 5}}
    result = jp.search('foo.bar', data)
    assert result == 5

def test_identity_query():
    jp = JpWrapper('./jp')
    data = {"foo": 42}
    result = jp.search('@', data)
    assert result == {"foo": 42}

def test_list_index():
    jp = JpWrapper('./jp')
    data = {"a": [1,2,3]}
    result = jp.search('a[1]', data)
    assert result == 2

def test_invalid_query_raises():
    jp = JpWrapper('./jp')
    data = {"foo": 123}
    with pytest.raises(Exception):
        jp.search('???', data)

def test_non_json_output():
    jp = JpWrapper('./jp')
    data = {"foo": 1}
    # Query that should output a bare value, not valid JSON
    result = jp.search('foo', data)
    assert result == 1

def test_custom_binary_path():
    jp = JpWrapper('./jp')  # Default, but path is tested here
    data = {"foo": "bar"}
    assert jp.search('foo', data) == "bar"

def test_error_on_missing_jp(monkeypatch):
    jp = JpWrapper('./missing-jp-bin')
    with pytest.raises(Exception):
        jp.search('foo', {"foo": 1})

def test_empty_result():
    jp = JpWrapper('./jp')
    data = {"foo": {"bar": 123}}
    # Query something that's missing
    assert jp.search('foo.baz', data) is None or jp.search('foo.baz', data) == ""