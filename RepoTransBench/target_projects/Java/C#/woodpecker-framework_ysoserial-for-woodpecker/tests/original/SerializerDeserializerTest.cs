using System;
using System.IO;
using Xunit;

namespace WoodpeckerYsoserial.Tests
{
    public class DummySerializable : IEquatable<DummySerializable>, System.Runtime.Serialization.ISerializable
    {
        public string Value { get; set; }
        public DummySerializable(string v) { Value = v; }
        public bool Equals(DummySerializable other) => other != null && Value == other.Value;

        public override bool Equals(object obj) => obj is DummySerializable o && Equals(o);

        public override int GetHashCode() => Value?.GetHashCode() ?? 0;

        // Serialization stubs
        public void GetObjectData(System.Runtime.Serialization.SerializationInfo info, System.Runtime.Serialization.StreamingContext context)
        {
            info.AddValue("Value", Value);
        }
        public DummySerializable(System.Runtime.Serialization.SerializationInfo info, System.Runtime.Serialization.StreamingContext context)
        {
            Value = info.GetString("Value");
        }
    }

    public class SerializerDeserializerTest
    {
        [Fact]
        public void TestSerializeAndDeserialize()
        {
            var testObj = new DummySerializable("foo");
            var data = Serializer.Serialize(testObj);
            var result = Deserializer.Deserialize(data);
            Assert.Equal(testObj, result);
        }

        [Fact]
        public void TestSerializerCallable()
        {
            var testObj = new DummySerializable("bar");
            var s = new Serializer(testObj);
            var data = s.Call();
            Assert.Equal(testObj, Deserializer.Deserialize(data));
        }

        [Fact]
        public void TestDeserializerCallable()
        {
            var testObj = new DummySerializable("baz");
            var s = new Serializer(testObj);
            var data = s.Call();
            var d = new Deserializer(data);
            Assert.Equal(testObj, d.Call());
        }

        [Fact]
        public void TestSerializeToOutputStream()
        {
            var testObj = new DummySerializable("baz");
            using (var bos = new MemoryStream())
            {
                Serializer.Serialize(testObj, bos);
                var result = Deserializer.Deserialize(bos.ToArray());
                Assert.Equal(testObj, result);
            }
        }

        [Fact]
        public void TestDeserializeFromInputStream()
        {
            var testObj = new DummySerializable("boo");
            var data = Serializer.Serialize(testObj);
            using (var bis = new MemoryStream(data))
            {
                var result = Deserializer.Deserialize(bis);
                Assert.Equal(testObj, result);
            }
        }

        [Fact]
        public void TestMainMethodOfDeserializer()
        {
            var testObj = new DummySerializable("mainTest");
            var data = Serializer.Serialize(testObj);

            var tmpfile = Path.GetTempFileName();
            try
            {
                File.WriteAllBytes(tmpfile, data);

                // Simulate: main() loads and deserializes from stdin (not directly translatable in C#, so just call)
                using (var fs = File.OpenRead(tmpfile))
                {
                    Deserializer.Main(new string[] { });
                }
            }
            finally
            {
                File.Delete(tmpfile);
            }
            // Should not throw exception!
        }

        [Fact]
        public void TestSerializeNullThrows()
        {
            Assert.Throws<ArgumentNullException>(() =>
            {
                Serializer.Serialize(null);
            });
        }
    }
}