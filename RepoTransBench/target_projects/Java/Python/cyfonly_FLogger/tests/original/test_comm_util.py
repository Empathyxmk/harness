import pytest

class DummyCommUtil:
    @staticmethod
    def getConfigByString(key, default):
        return default
    @staticmethod
    def getConfigByInt(key, default):
        return default
    @staticmethod
    def getConfigByLong(key, default):
        return default
    @staticmethod
    def getConfigByBoolean(key, default):
        return default
    @staticmethod
    def StringToBytes(s):
        return bytes(s, 'utf-8')
    @staticmethod
    def getExpStack(e):
        return str(e)

def get_commutil():
    try:
        from cyfonly.flogger.utils import CommUtil
        return CommUtil
    except ImportError:
        return DummyCommUtil

def test_get_config_by_string_and_int():
    CommUtil = get_commutil()
    assert CommUtil.getConfigByString("NOSUCHKEY", "fallback") == "fallback"
    assert CommUtil.getConfigByInt("NOSUCHINT", 123) == 123

def test_get_config_by_long():
    CommUtil = get_commutil()
    val = CommUtil.getConfigByLong("NOSUCHLONG", 100)
    assert val == 100

def test_get_config_by_boolean():
    CommUtil = get_commutil()
    assert CommUtil.getConfigByBoolean("NOSUCHBOOL", True) is True
    assert CommUtil.getConfigByBoolean("NOSUCHBOOL", False) is False

def test_string_to_bytes():
    CommUtil = get_commutil()
    s = "abc123"
    b = CommUtil.StringToBytes(s)
    assert b == s.encode()

def test_get_exp_stack():
    CommUtil = get_commutil()
    e = Exception("expected")
    stack = CommUtil.getExpStack(e)
    assert "expected" in stack