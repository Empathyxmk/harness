class ChannelInfo:
    def __init__(self, channel, extra_info):
        self.channel = channel
        self.extra_info = extra_info

    def __eq__(self, other):
        if not isinstance(other, ChannelInfo):
            return False
        return self.channel == other.channel and self.extra_info == other.extra_info

    def __hash__(self):
        return hash((self.channel, frozenset(self.extra_info.items()) if self.extra_info else None))

def test_equals_and_hash_code_public():
    extra_a = {"baz": "qux"}
    a = ChannelInfo("public", extra_a)
    b = ChannelInfo("public", extra_a)
    assert a == b
    assert hash(a) == hash(b)

    # different channel
    c = ChannelInfo("diff", extra_a)
    assert a != c

    # different extraInfo
    d = ChannelInfo("public", None)
    assert a != d

    # null channel
    e = ChannelInfo(None, extra_a)
    f = ChannelInfo(None, extra_a)
    assert e == f
    assert hash(e) == hash(f)