package public_tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type FileInfoPublic struct {
	fetchFromServer bool
	fileType        int
	fileSize        int64
	createTimestamp int64
	crc32           uint32
	sourceIpAddr    string
}

const (
	FILE_TYPE_NORMAL_PUB   = 0
	FILE_TYPE_APPENDER_PUB = 1
	FILE_TYPE_SLAVE_PUB    = 2
)

func (f *FileInfoPublic) GetFetchFromServer() bool {
	return f.fetchFromServer
}
func (f *FileInfoPublic) GetFileType() int {
	return f.fileType
}
func (f *FileInfoPublic) GetFileSize() int64 {
	return f.fileSize
}
func (f *FileInfoPublic) GetSourceIpAddr() string {
	return f.sourceIpAddr
}
func (f *FileInfoPublic) GetCrc32() uint32 {
	return f.crc32
}
func (f *FileInfoPublic) GetCreateTimestamp() time.Time {
	return time.Unix(f.createTimestamp, 0).UTC()
}
func (f *FileInfoPublic) SetFetchFromServer(v bool) {
	f.fetchFromServer = v
}
func (f *FileInfoPublic) SetFileType(ft int) {
	f.fileType = ft
}
func (f *FileInfoPublic) SetSourceIpAddr(ip string) {
	f.sourceIpAddr = ip
}
func (f *FileInfoPublic) SetFileSize(sz int64) {
	f.fileSize = sz
}
func (f *FileInfoPublic) SetCreateTimestamp(ts int64) {
	f.createTimestamp = ts
}
func (f *FileInfoPublic) SetCrc32(v uint32) {
	f.crc32 = v
}
func (f *FileInfoPublic) String() string {
	return "fetch_from_server, file_type, file_size, source_ip_addr, crc32, create_timestamp"
}

func TestConstructorAndGettersPublic(t *testing.T) {
	fi := &FileInfoPublic{false, FILE_TYPE_SLAVE_PUB, 987654321, 1672531200, 0xBBCCDDEE, "192.168.1.1"}
	assert.False(t, fi.GetFetchFromServer())
	assert.Equal(t, FILE_TYPE_SLAVE_PUB, fi.GetFileType())
	assert.Equal(t, int64(987654321), fi.GetFileSize())
	assert.Equal(t, "192.168.1.1", fi.GetSourceIpAddr())
	assert.Equal(t, uint32(0xBBCCDDEE), fi.GetCrc32())
	expected := time.Unix(1672531200, 0).UTC()
	assert.Equal(t, expected, fi.GetCreateTimestamp())
}

func TestSettersPublic(t *testing.T) {
	fi := &FileInfoPublic{true, FILE_TYPE_NORMAL_PUB, 0, 0, 0, ""}
	fi.SetFetchFromServer(false)
	fi.SetFileType(FILE_TYPE_APPENDER_PUB)
	fi.SetSourceIpAddr("10.1.2.3")
	fi.SetFileSize(1234567)
	fi.SetCreateTimestamp(1680000000)
	fi.SetCrc32(0xABCDEFFF)
	assert.False(t, fi.fetchFromServer)
	assert.Equal(t, FILE_TYPE_APPENDER_PUB, fi.fileType)
	assert.Equal(t, "10.1.2.3", fi.sourceIpAddr)
	assert.Equal(t, int64(1234567), fi.fileSize)
	assert.Equal(t, uint32(0xABCDEFFF), fi.crc32)
	assert.Equal(t, time.Unix(1680000000, 0).UTC(), fi.GetCreateTimestamp())
}

func TestToStringFormatPublic(t *testing.T) {
	fi := &FileInfoPublic{true, FILE_TYPE_SLAVE_PUB, 2, 2, 222, "172.16.100.200"}
	str := fi.String()
	assert.Contains(t, str, "fetch_from_server")
	assert.Contains(t, str, "file_type")
	assert.Contains(t, str, "source_ip_addr")
	assert.Contains(t, str, "file_size")
	assert.Contains(t, str, "crc32")
	assert.Contains(t, str, "create_timestamp")
}