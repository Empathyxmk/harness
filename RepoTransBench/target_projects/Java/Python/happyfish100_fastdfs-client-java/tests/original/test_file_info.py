from datetime import datetime

class FileInfo:
    FILE_TYPE_NORMAL = 0
    FILE_TYPE_APPENDER = 1
    FILE_TYPE_SLAVE = 2

    def __init__(self, fetch_from_server, file_type, file_size, create_timestamp, crc32, source_ip_addr):
        self._fetch_from_server = fetch_from_server
        self._file_type = file_type
        self._file_size = file_size
        self._create_timestamp = create_timestamp
        self._crc32 = crc32
        self._source_ip_addr = source_ip_addr

    def getFetchFromServer(self):
        return self._fetch_from_server

    def getFileType(self):
        return self._file_type

    def getFileSize(self):
        return self._file_size

    def getSourceIpAddr(self):
        return self._source_ip_addr

    def getCrc32(self):
        return self._crc32

    def getCreateTimestamp(self):
        return datetime.utcfromtimestamp(self._create_timestamp)

    def setFetchFromServer(self, val):
        self._fetch_from_server = val

    def setFileType(self, t):
        self._file_type = t

    def setFileSize(self, s):
        self._file_size = s

    def setCreateTimestamp(self, t):
        self._create_timestamp = t

    def setCrc32(self, val):
        self._crc32 = val

    def setSourceIpAddr(self, ip):
        self._source_ip_addr = ip

    def __str__(self):
        return "FileInfo(fetch_from_server={}, file_type={}, file_size={}, create_timestamp={}, crc32={}, source_ip_addr={})".format(
            self._fetch_from_server, self._file_type, self._file_size, self._create_timestamp, self._crc32, self._source_ip_addr)

def test_constructor_and_getters():
    fi = FileInfo(True, FileInfo.FILE_TYPE_NORMAL, 123456789, 1609459200, 0xAABBCCDD, "127.0.0.1")
    assert fi.getFetchFromServer() == True
    assert fi.getFileType() == FileInfo.FILE_TYPE_NORMAL
    assert fi.getFileSize() == 123456789
    assert fi.getSourceIpAddr() == "127.0.0.1"
    assert fi.getCrc32() == 0xAABBCCDD
    expected_date = datetime.utcfromtimestamp(1609459200)
    assert fi.getCreateTimestamp() == expected_date

def test_setters():
    fi = FileInfo(False, FileInfo.FILE_TYPE_APPENDER, 0, 0, 0, "")
    fi.setFetchFromServer(True)
    fi.setFileType(FileInfo.FILE_TYPE_SLAVE)
    fi.setSourceIpAddr("192.168.100.100")
    fi.setFileSize(1000000)
    fi.setCreateTimestamp(1620000000)
    fi.setCrc32(0xFFFFEEEE)
    assert fi.getFetchFromServer() == True
    assert fi.getFileType() == FileInfo.FILE_TYPE_SLAVE
    assert fi.getSourceIpAddr() == "192.168.100.100"
    assert fi.getFileSize() == 1000000
    assert fi.getCreateTimestamp() == datetime.utcfromtimestamp(1620000000)
    assert fi.getCrc32() == 0xFFFFEEEE

def test_to_string_format():
    fi = FileInfo(False, FileInfo.FILE_TYPE_NORMAL, 1, 1, 111, "10.0.0.1")
    s = str(fi)
    assert "fetch_from_server" in s
    assert "file_type" in s
    assert "source_ip_addr" in s
    assert "file_size" in s
    assert "crc32" in s
    assert "create_timestamp" in s