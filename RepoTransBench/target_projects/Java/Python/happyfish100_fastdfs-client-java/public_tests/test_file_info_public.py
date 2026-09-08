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

def test_constructor_and_getters_public():
    # Different file size, IP, CRC, timestamp
    fi = FileInfo(False, FileInfo.FILE_TYPE_SLAVE, 987654321, 1672531200, 0xBBCCDDEE, "192.168.1.1")
    assert fi.getFetchFromServer() is False
    assert fi.getFileType() == FileInfo.FILE_TYPE_SLAVE
    assert fi.getFileSize() == 987654321
    assert fi.getSourceIpAddr() == "192.168.1.1"
    assert fi.getCrc32() == 0xBBCCDDEE
    expected_date = datetime.utcfromtimestamp(1672531200)
    assert fi.getCreateTimestamp() == expected_date

def test_setters_public():
    fi = FileInfo(True, FileInfo.FILE_TYPE_NORMAL, 0, 0, 0, "")
    fi.setFetchFromServer(False)
    fi.setFileType(FileInfo.FILE_TYPE_APPENDER)
    fi.setSourceIpAddr("10.1.2.3")
    fi.setFileSize(1234567)
    fi.setCreateTimestamp(1680000000)
    fi.setCrc32(0xABCDEFFF)
    assert fi.getFetchFromServer() is False
    assert fi.getFileType() == FileInfo.FILE_TYPE_APPENDER
    assert fi.getSourceIpAddr() == "10.1.2.3"
    assert fi.getFileSize() == 1234567
    assert fi.getCreateTimestamp() == datetime.utcfromtimestamp(1680000000)
    assert fi.getCrc32() == 0xABCDEFFF

def test_to_string_format_public():
    fi = FileInfo(True, FileInfo.FILE_TYPE_SLAVE, 2, 2, 222, "172.16.100.200")
    s = str(fi)
    assert "fetch_from_server" in s
    assert "file_type" in s
    assert "source_ip_addr" in s
    assert "file_size" in s
    assert "crc32" in s
    assert "create_timestamp" in s