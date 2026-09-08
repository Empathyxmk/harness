def is_allowed(url):
    # Test filter logic:
    # Block URLs with .exe extension
    # Block no.go.com and any .exe
    if "no.go.com" in url:
        return False
    if url.endswith(".exe"):
        return False
    return True

def test_different_domain_url_allowed():
    assert is_allowed("https://anotherdomain.com/index.html")

def test_filtered_extension():
    assert not is_allowed("http://test.com/download/file.exe")

def test_complex_query_string():
    assert is_allowed("http://somedomain.com/page?search=stormcrawler&sort=desc")