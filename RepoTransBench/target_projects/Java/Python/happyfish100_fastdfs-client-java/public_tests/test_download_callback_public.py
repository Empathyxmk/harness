class TestDownloadCallback:
    def __init__(self):
        self.lastBytes = None
        self.lastFileSize = None
        self.lastData = None

    def recv(self, file_size, data, bytes_len):
        self.lastFileSize = file_size
        self.lastData = data
        self.lastBytes = bytes_len
        return 0

def test_callback_public():
    cb = TestDownloadCallback()
    data = bytes([10, 20, 30, 40, 50])
    result = cb.recv(987654321, data, len(data))
    assert result == 0
    assert cb.lastFileSize == 987654321
    assert cb.lastData == data
    assert cb.lastBytes == len(data)