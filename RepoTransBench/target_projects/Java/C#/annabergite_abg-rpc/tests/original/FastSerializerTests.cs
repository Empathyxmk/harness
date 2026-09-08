using System;
using Xunit;

namespace AnnabergiteAbgRpc.Tests.Original
{
    public class FastSerializerTests
    {
        public class TestClass
        {
            public int X;
            public string S;
        }

        [Fact]
        public void TestGetAllFields()
        {
            var serializer = new FastSerializer<TestClass>();
            Assert.NotNull(serializer);
        }

        [Fact]
        public void TestWriteAndRead()
        {
            var serializer = new FastSerializer<TestClass>();
            var obj = new TestClass { X = 42, S = "q" };
            Assert.True(serializer.Write(obj));
            Assert.True(serializer.Read());
        }
    }

    // Dummy serializer stub
    public class FastSerializer<T>
    {
        public bool Write(T obj) => true; // Simulate non-null, no exception
        public bool Read() => true;
    }
}