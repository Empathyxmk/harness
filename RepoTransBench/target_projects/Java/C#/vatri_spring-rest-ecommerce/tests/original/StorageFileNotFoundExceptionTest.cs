using Xunit;
using Vatri.Ecommerce.Storage;
using System;

namespace OriginalTests
{
    public class StorageFileNotFoundExceptionTest
    {
        [Fact]
        public void TestMessageConstructor()
        {
            var ex = new StorageFileNotFoundException("testmsg");
            Assert.Equal("testmsg", ex.Message);
        }

        [Fact]
        public void TestMessageAndCauseConstructor()
        {
            var cause = new Exception("inner");
            var ex = new StorageFileNotFoundException("outer", cause);
            Assert.Equal("outer", ex.Message);
            Assert.Equal(cause, ex.InnerException);
        }
    }
}