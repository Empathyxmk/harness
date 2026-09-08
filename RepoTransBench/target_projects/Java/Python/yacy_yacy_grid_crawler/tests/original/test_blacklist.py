import os
import tempfile
import re
import pytest

# Dummy implementation for Blacklist and MultiProtocolURL for testing purposes.
# In actual usage, these should be imported from the corresponding source modules.
class MultiProtocolURL:
    def __init__(self, url):
        self.url = url

    def toNormalform(self, _):
        return self.url

class Blacklist:
    class BlacklistInfo:
        def __init__(self, pattern, source, info, host):
            try:
                self.matcher = re.compile(pattern)
            except re.error as e:
                raise re.error(str(e))
            self.source = source
            self.info = info
            self.host = host

    def __init__(self):
        self.patterns = []
        self.cache_hit = set()
        self.cache_miss = set()

    def load(self, file_path):
        self.patterns = []
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("host "):
                    _, host, *_ = line.split()
                    pattern = re.escape(host)
                    try:
                        self.patterns.append(
                            self.BlacklistInfo(pattern, "host", "", host)
                        )
                    except re.error:
                        pass  # Logging is not implemented
                else:
                    pattern = line.split("#")[0].strip()
                    if not pattern:
                        continue
                    try:
                        self.patterns.append(
                            self.BlacklistInfo(pattern, "pattern", "", None)
                        )
                    except re.error:
                        pass  # Logging is not implemented

    def isBlacklisted(self, urlstr, urlobj):
        if urlstr in self.cache_hit:
            return True
        if urlstr in self.cache_miss:
            return None
        for info in self.patterns:
            if info.host:
                # Host matching
                if urlobj.url.find(info.host) >= 0:
                    self.cache_hit.add(urlstr)
                    return info
            else:
                if info.matcher.search(urlstr):
                    self.cache_hit.add(urlstr)
                    return info
        self.cache_miss.add(urlstr)
        return None

def test_load_plain_patterns(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "blacklist.txt"
    with test_file.open("w") as f:
        f.write(".*forbidden.com.* # info1\n")
        f.write("# this is a comment\n")
        f.write(".*blockme.net.*\n")
    blacklist.load(str(test_file))

    url1 = MultiProtocolURL("http://forbidden.com/page")
    url2 = MultiProtocolURL("http://blockme.net/")
    url3 = MultiProtocolURL("http://allowed.com/")
    assert blacklist.isBlacklisted(url1.toNormalform(True), url1) is not None
    assert blacklist.isBlacklisted(url2.toNormalform(True), url2) is not None
    assert blacklist.isBlacklisted(url3.toNormalform(True), url3) is None

def test_load_host_pattern(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "blacklist_host.txt"
    with test_file.open("w") as f:
        f.write("host example.com # host entry\n")
    blacklist.load(str(test_file))

    url = MultiProtocolURL("http://example.com/page")
    assert blacklist.isBlacklisted(url.toNormalform(True), url) is not None
    other = MultiProtocolURL("http://test.com/page")
    assert blacklist.isBlacklisted(other.toNormalform(True), other) is None

def test_pattern_syntax_error(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "badpattern.txt"
    with test_file.open("w") as f:
        f.write(".*this[is(bad\n")
    # Should log but not throw in load
    try:
        blacklist.load(str(test_file))
    except Exception as e:
        pytest.fail(f"Exception was raised in loading: {e}")

def test_blacklist_info_constructor_with_invalid_pattern():
    with pytest.raises(re.error):
        Blacklist.BlacklistInfo("*This is [invalid", "src", "", None)

def test_blacklist_caches(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "cachetest.txt"
    with test_file.open("w") as f:
        f.write(".*foo.com.*\n")
    blacklist.load(str(test_file))
    url = MultiProtocolURL("http://foo.com/bar")
    str_url = url.toNormalform(True)
    assert blacklist.isBlacklisted(str_url, url) is not None
    # Call second time to test cache
    assert blacklist.isBlacklisted(str_url, url) is not None

def test_blacklist_miss_cache(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "misscachetest.txt"
    with test_file.open("w") as f:
        f.write(".*nothingtomatch.net.*\n")
    blacklist.load(str(test_file))
    url = MultiProtocolURL("http://notfoo.com/")
    str_url = url.toNormalform(True)
    assert blacklist.isBlacklisted(str_url, url) is None
    # Should be cached now
    assert blacklist.isBlacklisted(str_url, url) is None

def test_blacklist_info_fields():
    bi = Blacklist.BlacklistInfo(".*test.com.*", "src", "information", "host.com")
    assert bi.matcher is not None
    assert bi.source == "src"
    assert bi.info == "information"
    assert bi.host == "host.com"