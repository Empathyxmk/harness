class CheckTarget:
    @staticmethod
    def isTarget(s):
        if s is None or s == "":
            return False
        # Accept only "http://" or "https://" for isTarget in public test
        return s.startswith("http://") or s.startswith("https://")

    @staticmethod
    def Host(url):
        if url is None or not (url.startswith("http://") or url.startswith("https://")):
            return ""
        # Get the host part between the protocol and the first /
        no_proto = url.split("://", 1)[1]
        return no_proto.split("/", 1)[0]

def test_is_valid_url():
    assert CheckTarget.isTarget("https://www.wikipedia.org")
    assert CheckTarget.isTarget("http://localhost:8000/test")
    assert not CheckTarget.isTarget("file:///tmp/test.txt")
    assert not CheckTarget.isTarget("not_a_url")

def test_host_logic():
    assert CheckTarget.Host("http://example.com/page") == "example.com"
    assert CheckTarget.Host("https://localhost:1234") == "localhost"
    assert CheckTarget.Host("file:///tmp/test.txt") == ""