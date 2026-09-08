import pytest
import os
from jp_wrapper import JpWrapper

def jp_exists():
    return os.path.isfile('./jp') and os.access('./jp', os.X_OK)

pytestmark = pytest.mark.skipif(
    not jp_exists(),
    reason="jp binary not available for wrapper tests"
)

def test_public_basic_select():
    jp = JpWrapper('./jp')
    data = {"alpha": {"beta": 9}}
    result = jp.search('alpha.beta', data)
    assert result == 9

def test_public_identity_query():
    jp = JpWrapper('./jp')
    data = {"bar": 17}
    result = jp.search('@', data)
    assert result == {"bar": 17}

def test_public_list_index():
    jp = JpWrapper('./jp')
    data = {"numbers": [10, 20, 30]}
    result = jp.search('numbers[2]', data)
    assert result == 30

def test_public_invalid_query_raises():
    jp = JpWrapper('./jp')
    data = {"bar": 987}
    with pytest.raises(Exception):
        jp.search('!!!', data)

def test_public_non_json_output():
    jp = JpWrapper('./jp')
    data = {"bar": 7}
    # Query that should output a bare value, not valid JSON
    result = jp.search('bar', data)
    assert result == 7

def test_public_custom_binary_path():
    jp = JpWrapper('./jp')  # Default, but path is tested here
    data = {"a": "b"}
    assert jp.search('a', data) == "b"

def test_public_error_on_missing_jp(monkeypatch):
    jp = JpWrapper('./not-found-jp-bin')
    with pytest.raises(Exception):
        jp.search('bar', {"bar": 4})

def test_public_empty_result():
    jp = JpWrapper('./jp')
    data = {"alpha": {"beta": 1234}}
    # Query something that's missing
    assert jp.search('alpha.gamma', data) is None or jp.search('alpha.gamma', data) == ""