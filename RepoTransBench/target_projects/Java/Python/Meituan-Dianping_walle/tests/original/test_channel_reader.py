class ChannelInfo:
    def __init__(self, channel, extra_info):
        self.channel = channel
        self.extra_info = extra_info

    def getChannel(self):
        return self.channel

    def getExtraInfo(self):
        return self.extra_info

class ChannelReader:
    @staticmethod
    def getChannel(file):
        # Returns None for None files or if doesn't exist (simulate)
        if file is None:
            return None
        return None

    @staticmethod
    def getChannelInfo(file):
        if file is None:
            return None
        return None

    @staticmethod
    def getChannelInfoMap(file):
        if file is None:
            return None
        return None

    @staticmethod
    def parseChannel(s):
        import json
        if s is None:
            return None
        try:
            obj = json.loads(s)
            channel = obj.get("channel")
            extra = obj.get("extra") if "extra" in obj else None
            return ChannelInfo(channel, extra)
        except Exception:
            return None

def test_get_channel_normal():
    file = None
    assert ChannelReader.getChannel(file) is None

def test_get_channel_info_normal():
    file = None
    assert ChannelReader.getChannelInfo(file) is None

def test_get_channel_info_map_null_file():
    file = None
    assert ChannelReader.getChannelInfoMap(file) is None

def test_parse_channel_null_string():
    assert ChannelReader.parseChannel(None) is None

def test_parse_channel_malformed():
    malformed = "{not-a-json}"
    assert ChannelReader.parseChannel(malformed) is None

def test_parse_channel_valid():
    json_str = '{"channel":"TestChannel","extra":{"foo":"bar"}}'
    info = ChannelReader.parseChannel(json_str)
    assert info is not None
    assert info.getChannel() == "TestChannel"
    assert info.getExtraInfo() is not None
    assert info.getExtraInfo().get("foo") == "bar"

def test_parse_channel_valid_no_extra():
    json_str = '{"channel":"A"}'
    info = ChannelReader.parseChannel(json_str)
    assert info is not None
    assert info.getChannel() == "A"
    assert info.getExtraInfo() is None

def test_parse_channel_valid_null_channel():
    json_str = '{"extra":{"foo":"bar"}}'
    info = ChannelReader.parseChannel(json_str)
    assert info is not None
    assert info.getChannel() is None
    assert info.getExtraInfo() is not None
    assert info.getExtraInfo().get("foo") == "bar"