using System;
using System.IO;
using System.Reflection;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.PublicTests
{
    public class PayloadReaderPublicTest
    {
        [Fact]
        public void TestGetString_NullFile_Public()
        {
            // Use a different non-existent file name
            var nonExistent = new FileInfo("definitely-not-an-apk-file-public.apk");
            string s = PayloadReader.GetString(nonExistent, 888888);
            Assert.Null(s);
        }

        [Fact]
        public void TestGetBytes_DifferentByteBuffer()
        {
            // Use a different buffer sequence and offset
            var method = typeof(PayloadReader).GetMethod("GetBytes", BindingFlags.NonPublic | BindingFlags.Static);
            byte[] data = new byte[] { 10, 20, 30, 40, 50, 60 };
            var buf = new ArraySegment<byte>(data, 2, 2); // [30,40]
            var buffer = new MemoryStream(buf.Array, buf.Offset, buf.Count);
            byte[] outBytes = (byte[])method.Invoke(null, new object[] { buffer });
            Assert.Equal(new byte[] { 30, 40 }, outBytes);
        }

        [Fact]
        public void TestGet_NullFile_ReturnsNull_Public()
        {
            var nonExistent = new FileInfo("another-fake-apk-file-public.apk");
            Assert.Null(PayloadReader.Get(nonExistent, 999999));
        }
    }
}