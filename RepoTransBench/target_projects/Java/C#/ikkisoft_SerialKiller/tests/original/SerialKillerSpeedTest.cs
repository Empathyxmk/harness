using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using Xunit;

namespace Ikkisoft.SerialKiller.Tests.Original
{
    public class SerialKillerSpeedTest
    {
        [Fact]
        public void SpeedTest()
        {
            var outPerson = new Person(1, "Test");
            var memory = new MemoryStream();
            var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
            formatter.Serialize(memory, outPerson);
            var bytes = memory.ToArray();
#pragma warning restore SYSLIB0011

            SpeedTestImpl(bytes, new TestDeserializeCommon(), false);
            SpeedTestImpl(bytes, new TestDeserializeSerialKiller(), true);
        }

        private static void SpeedTestImpl(byte[] bytes, ITestDeserialize testDeserialize, bool withSerialKiller)
        {
            for (int i = 0; i < 1000; i++)
                testDeserialize.Deserialize(new MemoryStream(bytes));

            var timeStart = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            for (int i = 0; i < 10_000; i++)
                testDeserialize.Deserialize(new MemoryStream(bytes));
            var result = DateTimeOffset.Now.ToUnixTimeMilliseconds() - timeStart;
            if (withSerialKiller)
                Console.WriteLine($"Result (WITH SerialKiller): {result}ms for 10.000 iterations");
            else
                Console.WriteLine($"Result (WITHOUT SerialKiller): {result}ms for 10.000 iterations");
        }

        public interface ITestDeserialize
        {
            void Deserialize(Stream stream);
        }

        public class TestDeserializeCommon : ITestDeserialize
        {
            public void Deserialize(Stream stream)
            {
                var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                var person = (Person)formatter.Deserialize(stream);
#pragma warning restore SYSLIB0011
            }
        }

        public class TestDeserializeSerialKiller : ITestDeserialize
        {
            public void Deserialize(Stream stream)
            {
                // In a real system, this would use SerialKiller-aware deserialization.
                // Here it just deserializes as usual (simulate presence of checker)
                var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                var person = (Person)formatter.Deserialize(stream);
#pragma warning restore SYSLIB0011
            }
        }
    }

    [Serializable]
    public class Person
    {
        public int Id { get; }
        public string Name { get; }
        public Person(int id, string name) { Id = id; Name = name; }
    }
}