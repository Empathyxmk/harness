class ChannelInfo:
    def __init__(self, channel, extra_info):
        self.channel = channel
        self.extra_info = extra_info

    def getChannel(self):
        return self.channel

    def getExtraInfo(self):
        return self.extra_info

    def __str__(self):
        return f"ChannelInfo(channel={self.channel}, extra_info={self.extra_info})"

def test_getters_and_to_string_public():
    info = {"testKey": "testVal"}
    channel_info = ChannelInfo("pub-channel", info)
    assert channel_info.getChannel() == "pub-channel"
    assert channel_info.getExtraInfo().get("testKey") == "testVal"
    s = str(channel_info)
    assert "pub-channel" in s
    assert "testKey" in s
    assert "testVal" in s

def test_null_extra_info_public():
    channel_info = ChannelInfo("pub-label", None)
    assert channel_info.getChannel() == "pub-label"
    assert channel_info.getExtraInfo() is None
    s = str(channel_info)
    assert "pub-label" in s
    assert "null" in s or "None" in s