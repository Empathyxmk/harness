import pytest
from cppstddb import log_level_info, log_level, log, log_impl

def test_log_level_names():
    assert log_level_info.get(log_level.error).name == "ERROR"
    assert log_level_info.get(log_level.warn).name == "WARN"
    assert log_level_info.get(log_level.debug).name == "DEBUG"

def test_log_level_get_by_name():
    assert log_level_info.get("NONE").level == log_level.none
    assert log_level_info.get("ERROR").level == log_level.error
    assert log_level_info.get("INFO").level == log_level.info

def test_log_level_bad_name_throws():
    import builtins
    with pytest.raises(RuntimeError):
        log_level_info.get("NOT_A_LEVEL")

def test_log_impl_level_set_and_is_enabled():
    lg = log()
    lg.level("INFO")
    assert lg.is_level_enabled(log_level.error)
    assert lg.is_level_enabled(log_level.info)
    assert not lg.is_level_enabled(log_level.debug)

def test_log_impl_operator_stream():
    # Assume __str__ or __repr__ for enum or class
    assert str(log_level.info) == "INFO"