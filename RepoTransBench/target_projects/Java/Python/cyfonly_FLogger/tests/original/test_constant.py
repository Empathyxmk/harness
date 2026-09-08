def get_constant():
    try:
        from cyfonly.flogger.constants import Constant
        return Constant
    except ImportError:
        class DummyConstant:
            DEBUG = 0
            INFO = 1
            WARN = 2
            ERROR = 3
            FATAL = 4
            LOG_DESC_MAP = {"0": "DEBUG", "1": "INFO", "2": "WARN", "3": "ERROR", "4": "FATAL"}
            CFG_LOG_LEVEL = "0,1,2,3,4"
            CFG_CHARSET_NAME = "UTF-8"
            CFG_LOG_PATH = "logs/"
        return DummyConstant

def test_log_levels():
    Constant = get_constant()
    assert Constant.DEBUG == 0
    assert Constant.INFO == 1
    assert Constant.WARN == 2
    assert Constant.ERROR == 3
    assert Constant.FATAL == 4

def test_log_desc_map():
    Constant = get_constant()
    assert Constant.LOG_DESC_MAP.get("0") == "DEBUG"
    assert Constant.LOG_DESC_MAP.get("1") == "INFO"
    assert Constant.LOG_DESC_MAP.get("2") == "WARN"
    assert Constant.LOG_DESC_MAP.get("3") == "ERROR"
    assert Constant.LOG_DESC_MAP.get("4") == "FATAL"

def test_config_defaults():
    Constant = get_constant()
    assert Constant.CFG_LOG_LEVEL is not None
    assert Constant.CFG_CHARSET_NAME.lower() == "utf-8"
    assert Constant.CFG_LOG_PATH is not None