using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using Xunit;

namespace Ikkisoft.SerialKiller.PublicTests
{
    public class SerialKillerPublicTest
    {
        [Fact]
        public void TestSerializationWithDifferentString()
        {
            var testStr = "PublicTestingStringXYZ";
            byte[] bytes;
            using (var ms = new MemoryStream())
            {
                var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                formatter.Serialize(ms, testStr);
#pragma warning restore SYSLIB0011
                bytes = ms.ToArray();
            }
            string result;
            using (var ms = new MemoryStream(bytes))
            {
                var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                result = (string)formatter.Deserialize(ms);
#pragma warning restore SYSLIB0011
            }
            Assert.Equal(testStr, result);
            Assert.False(string.IsNullOrEmpty(result));
            Assert.StartsWith("Public", result);
        }
    }
}