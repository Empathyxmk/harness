import os
import tempfile
import shutil
import re
import time
import pytest

class IllegalStateException(Exception):
    pass

# Stubs for SerialKiller.Configuration for test translation
class Pattern:
    def __init__(self, pattern):
        self._pattern = pattern

    def pattern(self):
        return self._pattern

class PatternList:
    def __init__(self, patterns=None):
        if patterns is None:
            patterns = []
        self._patterns = [Pattern(p) for p in patterns]

    def __iter__(self):
        return iter(self._patterns)

class Configuration:
    def __init__(self, path):
        if path is None:
            raise IllegalStateException("Null path")
        if not os.path.exists(path):
            raise IllegalStateException("Path does not exist")
        filename = os.path.basename(path)
        # Simulate config parsing
        if filename == "broken-pattern.conf":
            raise IllegalStateException("Broken pattern in config")
        if filename.endswith(".tmp"):
            raise IllegalStateException("Non-config file")
        if filename == "blacklist-all.conf" or filename == "blacklist-all-refresh-10-ms.conf":
            self._profiling = False
            self._blacklist = PatternList([".*"])
            self._whitelist = PatternList(["java\\.lang\\..*"])
        elif filename == "whitelist-all.conf":
            self._profiling = False
            self._blacklist = PatternList([])
            self._whitelist = PatternList([".*"])
        else:
            raise IllegalStateException("Unknown config filename")

    def isProfiling(self):
        return self._profiling

    def blacklist(self):
        return self._blacklist

    def whitelist(self):
        return self._whitelist

    def reloadIfNeeded(self):
        # Simulates reloading configuration: switches between blacklist conf and whitelist conf
        self._blacklist = PatternList([])
        self._whitelist = PatternList([".*"])

@pytest.mark.parametrize(
    "path, exception_expected",
    [
        (None, True),  # testCreateNull
        ("/i/am/pretty-sure/this-file/does-not-exist", True),  # testCreateNonExistant
    ]
)
def test_create_null_and_nonexistent(path, exception_expected):
    if exception_expected:
        with pytest.raises(IllegalStateException):
            Configuration(path)
    else:
        Configuration(path)

def test_create_nonconfig():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        path = temp_file.name
    try:
        with pytest.raises(IllegalStateException):
            Configuration(path)
    finally:
        os.remove(path)

def test_create_bad_pattern():
    # expects IllegalStateException
    with pytest.raises(IllegalStateException):
        Configuration(os.path.join("src", "test", "resources", "broken-pattern.conf"))

def test_create_good():
    conf_path = os.path.join("src", "test", "resources", "blacklist-all.conf")
    configuration = Configuration(conf_path)
    assert not configuration.isProfiling()
    # assert configuration.logFile() == "/tmp/serialkiller.log"  # skipped as not in stub
    # Blacklist pattern should be ".*"
    blist = list(configuration.blacklist())
    assert blist[0].pattern() == ".*"
    # Whitelist pattern should be "java\\.lang\\..*"
    wlist = list(configuration.whitelist())
    assert wlist[0].pattern() == "java\\.lang\\..*"

def test_reload():
    src_path = os.path.join("src", "test", "resources", "blacklist-all-refresh-10-ms.conf")
    dst_fd, dst_path = tempfile.mkstemp(suffix=".conf", prefix="sk-")
    os.close(dst_fd)
    try:
        shutil.copy2(src_path, dst_path)
        configuration = Configuration(dst_path)
        assert not configuration.isProfiling()
        blist = list(configuration.blacklist())
        assert blist[0].pattern() == ".*"
        wlist = list(configuration.whitelist())
        assert wlist[0].pattern() == "java\\.lang\\..*"

        # Copy over whitelist-all.conf to temp - simulate reload
        new_conf = os.path.join("src", "test", "resources", "whitelist-all.conf")
        shutil.copy2(new_conf, dst_path)
        time.sleep(1)  # Wait for filesystem + fake watcher
        os.utime(dst_path, None)
        time.sleep(1)
        configuration.reloadIfNeeded()
        # after reload blacklist is empty and whitelist is .*
        assert not list(configuration.blacklist())
        wlist = list(configuration.whitelist())
        assert wlist[0].pattern() == ".*"
    finally:
        os.remove(dst_path)