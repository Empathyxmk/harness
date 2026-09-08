using System;
using Xunit;
using FastDFSClient;

namespace FastDFSClient.PublicTests
{
    public class FileInfoPublicTest
    {
        [Fact]
        public void TestConstructorAndGettersPublic()
        {
            var fileInfo = new FileInfo(false, FileInfo.FILE_TYPE_SLAVE, 987654321L, 1672531200, 0xBBCCDDEE, "192.168.1.1");
            Assert.False(fileInfo.FetchFromServer);
            Assert.Equal(FileInfo.FILE_TYPE_SLAVE, fileInfo.FileType);
            Assert.Equal(987654321L, fileInfo.FileSize);
            Assert.Equal("192.168.1.1", fileInfo.SourceIpAddr);
            Assert.Equal(0xBBCCDDEEL, fileInfo.Crc32);
            DateTime expectedDate = DateTimeOffset.FromUnixTimeSeconds(1672531200L).UtcDateTime;
            Assert.Equal(expectedDate, fileInfo.CreateTimestamp);
        }

        [Fact]
        public void TestSettersPublic()
        {
            var fileInfo = new FileInfo(true, FileInfo.FILE_TYPE_NORMAL, 0, 0, 0, "");
            fileInfo.FetchFromServer = false;
            fileInfo.FileType = FileInfo.FILE_TYPE_APPENDER;
            fileInfo.SourceIpAddr = "10.1.2.3";
            fileInfo.FileSize = 1234567L;
            fileInfo.CreateTimestamp = DateTimeOffset.FromUnixTimeSeconds(1680000000L).UtcDateTime;
            fileInfo.Crc32 = 0xABCDEFFF;
            Assert.False(fileInfo.FetchFromServer);
            Assert.Equal(FileInfo.FILE_TYPE_APPENDER, fileInfo.FileType);
            Assert.Equal("10.1.2.3", fileInfo.SourceIpAddr);
            Assert.Equal(1234567L, fileInfo.FileSize);
            Assert.Equal(DateTimeOffset.FromUnixTimeSeconds(1680000000L).UtcDateTime, fileInfo.CreateTimestamp);
            Assert.Equal(0xABCDEFFFL, fileInfo.Crc32);
        }

        [Fact]
        public void TestToStringFormatPublic()
        {
            var fileInfo = new FileInfo(true, FileInfo.FILE_TYPE_SLAVE, 2, 2, 222, "172.16.100.200");
            string str = fileInfo.ToString();
            Assert.Contains("fetch_from_server", str);
            Assert.Contains("file_type", str);
            Assert.Contains("source_ip_addr", str);
            Assert.Contains("file_size", str);
            Assert.Contains("crc32", str);
            Assert.Contains("create_timestamp", str);
        }
    }
}