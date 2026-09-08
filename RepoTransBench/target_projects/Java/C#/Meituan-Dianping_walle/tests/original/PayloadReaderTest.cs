using System;
using System.IO;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.Tests
{
    public class PayloadReaderTest
    {
        [Fact]
        public void TestGetString_NullFile()
        {
            // Non-existent file should return null (IOException + catch return null)
            FileInfo nonExistent = new FileInfo("not-a-real-apk-file.apk");
            string s = PayloadReader.GetString(nonExistent, 123);
            Assert.Null(s);
        }

        [Fact]
        public void TestGetBytes_NullByteBuffer()
        {
            // Simulate invocation of private static method GetBytes with restricted buffer
            var method = typeof(PayloadReader).GetMethod("GetBytes", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static);
            byte[] data = new byte[] { 1, 2, 3, 4, 5 };
            var buf = new ArraySegment<byte>(data, 1, 3); // [2,3,4]
            var buffer = new System.IO.MemoryStream(buf.Array, buf.Offset, buf.Count);
            byte[] outBytes = (byte[])method.Invoke(null, new object[] { buffer });
            Assert.Equal(new byte[] { 2, 3, 4 }, outBytes);
        }

        [Fact]
        public void TestGet_NullFile_ReturnsNull()
        {
            FileInfo nonExistent = new FileInfo("not-a-real-apk-file.apk");
            Assert.Null(PayloadReader.Get(nonExistent, 123));
        }
    }
}