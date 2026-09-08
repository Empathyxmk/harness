using System;
using System.IO;
using Xunit;

namespace WoodpeckerYsoserial.Tests
{
    public class SerializerDeserializerSmokeTest
    {
        [Fact]
        public void TestSerializerNullOutputStream()
        {
            Assert.Throws<ArgumentNullException>(() =>
            {
                Serializer.Serialize((Stream)null, new object());
            });
        }

        [Fact]
        public void TestSerializerNullObject()
        {
            using (var bos = new MemoryStream())
            {
                // Acceptable to throw
                Assert.ThrowsAny<Exception>(() => Serializer.Serialize(bos, null));
            }
        }

        [Fact]
        public void TestDeserializerNullInputStream()
        {
            Assert.Throws<ArgumentNullException>(() =>
            {
                Deserializer.Deserialize((Stream)null);
            });
        }

        [Fact]
        public void TestDeserializerBogusData()
        {
            var bogus = new byte[] { 1, 2, 3, 4 };
            using (var bis = new MemoryStream(bogus))
            {
                Assert.ThrowsAny<Exception>(() => Deserializer.Deserialize(bis));
            }
        }
    }
}