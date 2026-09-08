using Xunit;
using System;
using Vatri.Ecommerce.Storage;

namespace PublicTests
{
    public class StorageFileNotFoundExceptionPublicTest
    {
        [Fact]
        public void TestMessageConstructorPublic()
        {
            var ex = new StorageFileNotFoundException("public-message");
            Assert.Equal("public-message", ex.Message);
        }

        [Fact]
        public void TestMessageAndCauseConstructorPublic()
        {
            var cause = new Exception("different-inner");
            var ex = new StorageFileNotFoundException("different-outer", cause);
            Assert.Equal("different-outer", ex.Message);
            Assert.Equal(cause, ex.InnerException);
        }
    }
}