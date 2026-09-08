using System;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.PublicTests
{
    public class SignatureNotFoundExceptionPublicTest
    {
        [Fact]
        public void TestConstructorMessage_Public()
        {
            var ex = new SignatureNotFoundException("another message");
            Assert.Equal("another message", ex.Message);
            Assert.Null(ex.InnerException);
        }

        [Fact]
        public void TestConstructorMessageAndCause_Public()
        {
            Exception cause = new NullReferenceException("public cause");
            var ex = new SignatureNotFoundException("public error", cause);
            Assert.Equal("public error", ex.Message);
            Assert.Equal(cause, ex.InnerException);
        }
    }
}