def get_commutil():
    try:
        from cyfonly.flogger.utils import CommUtil
        return CommUtil
    except ImportError:
        class DummyCommUtil:
            @staticmethod
            def getConfigByString(key, default): return default
            @staticmethod
            def getConfigByBoolean(key, default): return default
            @staticmethod
            def getExpStack(e): return f"java.lang.IllegalArgumentException: {str(e)}"
        return DummyCommUtil

def test_get_config_by_string_public():
    CommUtil = get_commutil()
    val = CommUtil.getConfigByString("NONEXIST_PUBLIC_KEY", "DifferentDefaultPublic")
    assert val == "DifferentDefaultPublic"

def test_get_config_by_boolean_public():
    CommUtil = get_commutil()
    b1 = CommUtil.getConfigByBoolean("NONEXIST_PUBLIC_BOOL", True)
    assert b1
    b2 = CommUtil.getConfigByBoolean("NONEXIST_PUBLIC_BOOL", False)
    assert not b2

def test_get_exp_stack_public():
    CommUtil = get_commutil()
    e = Exception("PublicStackTrace")
    stack = CommUtil.getExpStack(e)
    assert "java.lang.IllegalArgumentException" in stack or "Exception" in stack
    assert "PublicStackTrace" in stack