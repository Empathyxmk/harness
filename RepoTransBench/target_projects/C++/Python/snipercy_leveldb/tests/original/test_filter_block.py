def test_filter_block():
    # Simulate filter block builder/reader logic
    # Not a real implementation; for demonstration
    class SimpleFilter:
        def __init__(self):
            self.values = set()
        def add(self, key):
            self.values.add(key)
        def may_match(self, key):
            return key in self.values
    # Build filter
    f = SimpleFilter()
    f.add("foo")
    f.add("bar")
    f.add("box")
    assert f.may_match("foo")
    assert f.may_match("bar")
    assert not f.may_match("hello")
    assert not f.may_match("baz")