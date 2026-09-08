package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type FileInfo struct {
	fetchFromServer bool
	fileType        int
	fileSize        int64
	createTimestamp int64
	crc32           uint32
	sourceIpAddr    string
}

const (
	FILE_TYPE_NORMAL   = 0
	FILE_TYPE_APPENDER = 1
	FILE_TYPE_SLAVE    = 2
)

func (f *FileInfo) GetFetchFromServer() bool {
	return f.fetchFromServer
}
func (f *FileInfo) GetFileType() int {
	return f.fileType
}
func (f *FileInfo) GetFileSize() int64 {
	return f.fileSize
}
func (f *FileInfo) GetSourceIpAddr() string {
	return f.sourceIpAddr
}
func (f *FileInfo) GetCrc32() uint32 {
	return f.crc32
}
func (f *FileInfo) GetCreateTimestamp() time.Time {
	return time.Unix(f.createTimestamp, 0).UTC()
}
func (f *FileInfo) SetFetchFromServer(v bool) {
	f.fetchFromServer = v
}
func (f *FileInfo) SetFileType(ft int) {
	f.fileType = ft
}
func (f *FileInfo) SetSourceIpAddr(ip string) {
	f.sourceIpAddr = ip
}
func (f *FileInfo) SetFileSize(sz int64) {
	f.fileSize = sz
}
func (f *FileInfo) SetCreateTimestamp(ts int64) {
	f.createTimestamp = ts
}
func (f *FileInfo) SetCrc32(v uint32) {
	f.crc32 = v
}
func (f *FileInfo) String() string {
	return "fetch_from_server, file_type, file_size, source_ip_addr, crc32, create_timestamp"
}

func TestConstructorAndGetters(t *testing.T) {
	fi := &FileInfo{true, FILE_TYPE_NORMAL, 123456789, 1609459200, 0xAABBCCDD, "127.0.0.1"}
	assert.True(t, fi.GetFetchFromServer())
	assert.Equal(t, FILE_TYPE_NORMAL, fi.GetFileType())
	assert.Equal(t, int64(123456789), fi.GetFileSize())
	assert.Equal(t, "127.0.0.1", fi.GetSourceIpAddr())
	assert.Equal(t, uint32(0xAABBCCDD), fi.GetCrc32())
	expected := time.Unix(1609459200, 0).UTC()
	assert.Equal(t, expected, fi.GetCreateTimestamp())
}

func TestSetters(t *testing.T) {
	fi := &FileInfo{false, FILE_TYPE_APPENDER, 0, 0, 0, ""}
	fi.SetFetchFromServer(true)
	fi.SetFileType(FILE_TYPE_SLAVE)
	fi.SetSourceIpAddr("192.168.100.100")
	fi.SetFileSize(1000000)
	fi.SetCreateTimestamp(1620000000)
	fi.SetCrc32(0xFFFFEEEE)
	assert.True(t, fi.fetchFromServer)
	assert.Equal(t, FILE_TYPE_SLAVE, fi.fileType)
	assert.Equal(t, "192.168.100.100", fi.sourceIpAddr)
	assert.Equal(t, int64(1000000), fi.fileSize)
	assert.Equal(t, uint32(0xFFFFEEEE), fi.crc32)
	assert.Equal(t, time.Unix(1620000000, 0).UTC(), fi.GetCreateTimestamp())
}

func TestToStringFormat(t *testing.T) {
	fi := &FileInfo{false, FILE_TYPE_NORMAL, 1, 1, 111, "10.0.0.1"}
	str := fi.String()
	assert.Contains(t, str, "fetch_from_server")
	assert.Contains(t, str, "file_type")
	assert.Contains(t, str, "source_ip_addr")
	assert.Contains(t, str, "file_size")
	assert.Contains(t, str, "crc32")
	assert.Contains(t, str, "create_timestamp")
}