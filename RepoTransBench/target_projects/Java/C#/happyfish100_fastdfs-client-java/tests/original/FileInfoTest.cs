using System;
using Xunit;
using FastDFSClient;

namespace FastDFSClient.Tests
{
    public class FileInfoTest
    {
        [Fact]
        public void TestConstructorAndGetters()
        {
            var fileInfo = new FileInfo(true, FileInfo.FILE_TYPE_NORMAL, 123456789L, 1609459200, 0xAABBCCDD, "127.0.0.1");
            Assert.True(fileInfo.FetchFromServer);
            Assert.Equal(FileInfo.FILE_TYPE_NORMAL, fileInfo.FileType);
            Assert.Equal(123456789L, fileInfo.FileSize);
            Assert.Equal("127.0.0.1", fileInfo.SourceIpAddr);
            Assert.Equal(0xAABBCCDDL, fileInfo.Crc32);
            DateTime expectedDate = DateTimeOffset.FromUnixTimeSeconds(1609459200L).UtcDateTime;
            Assert.Equal(expectedDate, fileInfo.CreateTimestamp);
        }

        [Fact]
        public void TestSetters()
        {
            var fileInfo = new FileInfo(false, FileInfo.FILE_TYPE_APPENDER, 0, 0, 0, "");
            fileInfo.FetchFromServer = true;
            fileInfo.FileType = FileInfo.FILE_TYPE_SLAVE;
            fileInfo.SourceIpAddr = "192.168.100.100";
            fileInfo.FileSize = 1000000L;
            fileInfo.CreateTimestamp = DateTimeOffset.FromUnixTimeSeconds(1620000000L).UtcDateTime;
            fileInfo.Crc32 = 0xFFFFEEEE;
            Assert.True(fileInfo.FetchFromServer);
            Assert.Equal(FileInfo.FILE_TYPE_SLAVE, fileInfo.FileType);
            Assert.Equal("192.168.100.100", fileInfo.SourceIpAddr);
            Assert.Equal(1000000L, fileInfo.FileSize);
            Assert.Equal(DateTimeOffset.FromUnixTimeSeconds(1620000000L).UtcDateTime, fileInfo.CreateTimestamp);
            Assert.Equal(0xFFFFEEEEL, fileInfo.Crc32);
        }

        [Fact]
        public void TestToStringFormat()
        {
            var fileInfo = new FileInfo(false, FileInfo.FILE_TYPE_NORMAL, 1, 1, 111, "10.0.0.1");
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