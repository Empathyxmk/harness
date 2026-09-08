using System;
using Xunit;

namespace AnnabergiteAbgRpc.Tests.Original
{
    public class ByteBufOutputTests
    {
        [Fact]
        public void TestConstructorSetBuffer()
        {
            var buf = new MockByteBuf(8);
            var outBuf = new ByteBufOutput(buf);
            Assert.NotNull(outBuf);
            outBuf.SetBuffer(null); // Should not throw
        }

        [Fact]
        public void TestSetBufferWithCapacity()
        {
            var buf = new MockByteBuf(8);
            var outBuf = new ByteBufOutput(buf);
            outBuf.SetBuffer(buf, -1); // maxCapacity = safe max
            Assert.Throws<ArgumentException>(() => outBuf.SetBuffer(buf, -2));
        }

        [Fact]
        public void TestWriteAndRelease()
        {
            var buf = new MockByteBuf(4);
            var outBuf = new ByteBufOutput(buf);
            outBuf.Write(65);
            Assert.Equal(1, buf.ReadableBytes);
            outBuf.Release();
            Assert.Null(outBuf.ByteBuf);
        }
    }

    // Mock ByteBuf and ByteBufOutput classes
    public class MockByteBuf
    {
        private int _capacity;
        public int ReadableBytes { get; private set; }
        public MockByteBuf(int capacity) => _capacity = capacity;
        public void WriteByte(byte v) { ReadableBytes++; }
    }

    public class ByteBufOutput
    {
        public MockByteBuf ByteBuf { get; private set; }
        public ByteBufOutput(MockByteBuf buf) { ByteBuf = buf; }
        public void SetBuffer(MockByteBuf buf, int maxCapacity = -1)
        {
            if (maxCapacity < -1)
                throw new ArgumentException();
            ByteBuf = buf;
        }
        public void Write(int v) { ByteBuf?.WriteByte((byte)v); }
        public void SetBuffer(MockByteBuf? buf) { ByteBuf = buf; }
        public void Release() { ByteBuf = null; }
    }
}