using System;
using System.IO;
using Xunit;

namespace GoogleMailImporter.Tests.Original
{
    public class IoProviderTests
    {
        private class DummyIoProvider : IIoProvider<string>
        {
            private readonly bool _throwException;
            public DummyIoProvider(bool throwException) { _throwException = throwException; }
            public string Get()
            {
                if (_throwException)
                    throw new IOException("fail");
                return "success";
            }
        }

        [Fact]
        public void TestGetSuccess()
        {
            IIoProvider<string> ioProvider = new DummyIoProvider(false);
            Assert.Equal("success", ioProvider.Get());
        }

        [Fact]
        public void TestGetThrowsIOException()
        {
            IIoProvider<string> ioProvider = new DummyIoProvider(true);
            Assert.Throws<IOException>(() => ioProvider.Get());
        }
    }

    public interface IIoProvider<T>
    {
        T Get();
    }
}