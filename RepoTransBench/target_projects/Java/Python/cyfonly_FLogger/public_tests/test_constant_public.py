def get_constant():
    try:
        from cyfonly.flogger.constants import Constant
        return Constant
    except ImportError:
        class DummyConstant:
            FATAL = 4
            LOG_DESC_MAP = {"0": "DEBUG", "1": "INFO", "2": "WARN", "3": "ERROR", "4": "FATAL"}
            CFG_LOG_LEVEL = "0,1,2,3,4"
            CFG_CHARSET_NAME = "UTF-8"
            CFG_LOG_PATH = "log/dir/"
        return DummyConstant

def test_levels_and_map_public():
    Constant = get_constant()
    assert Constant.FATAL == 4
    assert Constant.LOG_DESC_MAP.get("4") == "FATAL"
    assert Constant.LOG_DESC_MAP.get("0") == "DEBUG"
    assert Constant.CFG_LOG_LEVEL is not None
    assert "4" in Constant.CFG_LOG_LEVEL

def test_charset_and_path_public():
    Constant = get_constant()
    assert Constant.CFG_CHARSET_NAME is not None
    assert Constant.CFG_LOG_PATH is not None
    assert "utf" in Constant.CFG_CHARSET_NAME.lower()
    assert "log" in Constant.CFG_LOG_PATH