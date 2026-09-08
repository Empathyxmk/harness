class ChannelReader:
    @staticmethod
    def getChannel(file):
        return None

    @staticmethod
    def getChannelInfo(file):
        return None

def test_get_channel_by_file_public():
    file = "nonexistent-public.apk"
    assert ChannelReader.getChannel(file) is None

def test_get_channel_info_by_file_public():
    file = "not-there-and-public.apk"
    assert ChannelReader.getChannelInfo(file) is None