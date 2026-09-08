using Xunit;
using FastDFSClient;

namespace FastDFSClient.PublicTests
{
    public class DownloadCallbackPublicTest
    {
        private class TestDownloadCallback : IDownloadCallback
        {
            public int lastBytes;
            public long lastFileSize;
            public byte[] lastData;

            public int Recv(long file_size, byte[] data, int bytes)
            {
                this.lastFileSize = file_size;
                this.lastData = data;
                this.lastBytes = bytes;
                return 0;
            }
        }

        [Fact]
        public void TestCallbackPublic()
        {
            var cb = new TestDownloadCallback();
            byte[] data = { 10, 20, 30, 40, 50 };
            int bytes = cb.Recv(987654321L, data, data.Length);
            Assert.Equal(0, bytes);
            Assert.Equal(987654321L, cb.lastFileSize);
            Assert.Equal(data, cb.lastData);
            Assert.Equal(data.Length, cb.lastBytes);
        }
    }
}