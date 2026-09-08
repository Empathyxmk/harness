from qcore.caching import cached_property

class DemoClass:
    def __init__(self):
        self.call_count = 0

    @cached_property
    def demo_attr(self):
        self.call_count += 1
        return "val" + str(self.call_count)

def test_public_cached_property_behavior():
    d = DemoClass()
    v1 = d.demo_attr
    v2 = d.demo_attr
    assert v1 == v2
    assert d.call_count == 1
    del d.demo_attr
    v3 = d.demo_attr
    assert v3 == "val2"
    assert d.call_count == 2