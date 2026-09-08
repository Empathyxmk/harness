def test_target_create_and_geturl_public():
    class Target:
        def __init__(self, url, target_class):
            self.url = url
            self.target_class = target_class
        def get_url(self):
            return self.url
        def get_target_class(self):
            return self.target_class
    target = Target("foo://bar", "SomeClass")
    assert target.get_url() == "foo://bar"
    assert target.get_target_class() == "SomeClass"

def test_target_set_url_public():
    class Target:
        def __init__(self, url, target_class):
            self.url = url
            self.target_class = target_class
        def set_url(self, url):
            self.url = url
        def get_url(self):
            return self.url
    target = Target("foo://baz", "OtherClass")
    target.set_url("foo://changed")
    assert target.get_url() == "foo://changed"