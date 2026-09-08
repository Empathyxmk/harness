using System.IO;
using Xunit;

namespace WoodpeckerYsoserial.PublicTests
{
    [System.Serializable]
    internal class Dummy
    {
        public string Value { get; private set; }
        public Dummy(string value) { Value = value; }
    }

    public class SerializerDeserializerPublicTest
    {
        [Fact]
        public void TestSerializeDeserializeSimple()
        {
            var dummy = new Dummy("public_test_1");
            using (var ms = new MemoryStream())
            {
                Serializer.Serialize(dummy, ms);
                ms.Seek(0, SeekOrigin.Begin);
                var obj = Deserializer.Deserialize(ms);
                Assert.True(obj is Dummy);
                Assert.Equal("public_test_1", ((Dummy)obj).Value);
            }
        }

        [Fact]
        public void TestSerializeDeserializeNull()
        {
            using (var ms = new MemoryStream())
            {
                Serializer.Serialize(null, ms);
                ms.Seek(0, SeekOrigin.Begin);
                var obj = Deserializer.Deserialize(ms);
                Assert.Null(obj);
            }
        }
    }
}