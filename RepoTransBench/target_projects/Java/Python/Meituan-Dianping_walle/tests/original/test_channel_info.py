class ChannelInfo:
    def __init__(self, channel, extra_info):
        self.channel = channel
        self.extra_info = extra_info

    def getChannel(self):
        return self.channel

    def getExtraInfo(self):
        return self.extra_info

def test_constructor_and_getters_basic():
    extra = {"k1": "v1"}
    info = ChannelInfo("channelA", extra)
    assert info.getChannel() == "channelA"
    assert info.getExtraInfo() == extra

def test_constructor_and_getters_null_extra():
    info = ChannelInfo("abc", None)
    assert info.getChannel() == "abc"
    assert info.getExtraInfo() is None

def test_constructor_and_getters_null_channel():
    extra = {}
    info = ChannelInfo(None, extra)
    assert info.getChannel() is None
    assert info.getExtraInfo() == extra