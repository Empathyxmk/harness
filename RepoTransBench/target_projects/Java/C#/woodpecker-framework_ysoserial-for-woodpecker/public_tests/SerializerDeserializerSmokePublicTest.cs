using System;
using System.IO;
using Xunit;

namespace WoodpeckerYsoserial.PublicTests
{
    [Serializable]
    internal class TestObj
    {
        public int N { get; private set; }
        public TestObj(int n) { N = n; }
    }

    public class SerializerDeserializerSmokePublicTest
    {
        [Fact]
        public void TestIntSerialization()
        {
            var obj = new TestObj(9876);
            using (var outStream = new MemoryStream())
            {
                Serializer.Serialize(obj, outStream);
                var inStream = new MemoryStream(outStream.ToArray());
                var o = Deserializer.Deserialize(inStream);
                Assert.IsType<TestObj>(o);
                Assert.Equal(9876, ((TestObj)o).N);
            }
        }
    }
}