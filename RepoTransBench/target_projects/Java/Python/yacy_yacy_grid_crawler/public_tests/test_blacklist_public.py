import re
import pytest

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
                        pass  # Logging not implemented
                else:
                    pattern = line.split("#")[0].strip()
                    if not pattern:
                        continue
                    try:
                        self.patterns.append(
                            self.BlacklistInfo(pattern, "pattern", "", None)
                        )
                    except re.error:
                        pass  # Logging not implemented

    def isBlacklisted(self, urlstr, urlobj):
        if urlstr in self.cache_hit:
            return True
        if urlstr in self.cache_miss:
            return None
        for info in self.patterns:
            if info.host:
                if urlobj.url.find(info.host) >= 0:
                    self.cache_hit.add(urlstr)
                    return info
            else:
                if info.matcher.search(urlstr):
                    self.cache_hit.add(urlstr)
                    return info
        self.cache_miss.add(urlstr)
        return None

def test_load_plain_patterns_public(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "public_blacklist.txt"
    with test_file.open("w") as f:
        f.write(".*denythis.org.* # info2\n")
        f.write("# another comment\n")
        f.write(".*lockme.io.*\n")
    blacklist.load(str(test_file))

    url1 = MultiProtocolURL("http://denythis.org/document")
    url2 = MultiProtocolURL("http://lockme.io/data")
    url3 = MultiProtocolURL("http://good.com/")
    assert blacklist.isBlacklisted(url1.toNormalform(True), url1) is not None
    assert blacklist.isBlacklisted(url2.toNormalform(True), url2) is not None
    assert blacklist.isBlacklisted(url3.toNormalform(True), url3) is None

def test_load_host_pattern_public(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "public_blacklist_host.txt"
    with test_file.open("w") as f:
        f.write("host othersite.org # public host entry\n")
    blacklist.load(str(test_file))

    url = MultiProtocolURL("http://othersite.org/info")
    assert blacklist.isBlacklisted(url.toNormalform(True), url) is not None
    other = MultiProtocolURL("http://diffsite.org/home")
    assert blacklist.isBlacklisted(other.toNormalform(True), other) is None

def test_pattern_syntax_error_public(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "public_badpattern.txt"
    with test_file.open("w") as f:
        f.write(".*wrong(syntax\n")
    try:
        blacklist.load(str(test_file))
    except Exception as e:
        pytest.fail(f"Exception was raised in loading: {e}")

def test_blacklist_info_constructor_with_invalid_pattern_public():
    with pytest.raises(re.error):
        Blacklist.BlacklistInfo("*Wrong [pattern", "src2", "", None)

def test_blacklist_caches_public(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "public_cachetest.txt"
    with test_file.open("w") as f:
        f.write(".*bar.org.*\n")
    blacklist.load(str(test_file))
    url = MultiProtocolURL("http://bar.org/example")
    str_url = url.toNormalform(True)
    assert blacklist.isBlacklisted(str_url, url) is not None
    assert blacklist.isBlacklisted(str_url, url) is not None

def test_blacklist_miss_cache_public(tmp_path):
    blacklist = Blacklist()
    test_file = tmp_path / "public_misscachetest.txt"
    with test_file.open("w") as f:
        f.write(".*abcxyz42.com.*\n")
    blacklist.load(str(test_file))
    url = MultiProtocolURL("http://notbar.org/home")
    str_url = url.toNormalform(True)
    assert blacklist.isBlacklisted(str_url, url) is None
    assert blacklist.isBlacklisted(str_url, url) is None

def test_blacklist_info_fields_public():
    bi = Blacklist.BlacklistInfo(".*another-test.org.*", "srcFile", "extra-info", "host.org")
    assert bi.matcher is not None
    assert bi.source == "srcFile"
    assert bi.info == "extra-info"
    assert bi.host == "host.org"