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

def test_recv():
    cb = TestDownloadCallback()
    data = bytes([1,2,3])
    result = cb.recv(123, data, len(data))
    assert result == 0
    assert cb.lastFileSize == 123
    assert cb.lastData == data
    assert cb.lastBytes == len(data)