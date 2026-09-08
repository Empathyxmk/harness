using Xunit;
using FastDFSClient;

namespace FastDFSClient.Tests
{
    public class DownloadCallbackTest
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
        public void TestRecv()
        {
            var callback = new TestDownloadCallback();
            byte[] data = new byte[] { 1, 2, 3 };
            int result = callback.Recv(123L, data, data.Length);

            Assert.Equal(0, result);
            Assert.Equal(123L, callback.lastFileSize);
            Assert.Equal(data, callback.lastData);
            Assert.Equal(data.Length, callback.lastBytes);
        }
    }
}