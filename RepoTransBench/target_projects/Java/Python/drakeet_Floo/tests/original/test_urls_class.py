def test_is_remote_url():
    def is_remote_url(url):
        if not url:
            return False
        return url.startswith("http://") or url.startswith("https://")
    assert is_remote_url("http://example.com")
    assert is_remote_url("https://secure.com")
    assert not is_remote_url("file://local.txt")     
    assert not is_remote_url("content://file")      
    assert not is_remote_url(None)
    assert not is_remote_url("")

def test_is_local_url():
    def is_local_url(url):
        if not url:
            return False
        return url.startswith("file://") or url.startswith("content://")
    assert is_local_url("file://localfile.txt")
    assert is_local_url("content://local")
    assert not is_local_url("http://remote.net")
    assert not is_local_url("https://secure.com")
    assert not is_local_url(None)
    assert not is_local_url("")