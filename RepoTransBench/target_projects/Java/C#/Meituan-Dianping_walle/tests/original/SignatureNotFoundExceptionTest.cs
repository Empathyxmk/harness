using System;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.Tests
{
    public class SignatureNotFoundExceptionTest
    {
        [Fact]
        public void TestConstructorMessage()
        {
            var ex = new SignatureNotFoundException("test message");
            Assert.Equal("test message", ex.Message);
            Assert.Null(ex.InnerException);
        }

        [Fact]
        public void TestConstructorMessageAndCause()
        {
            Exception cause = new InvalidOperationException("cause");
            var ex = new SignatureNotFoundException("err", cause);
            Assert.Equal("err", ex.Message);
            Assert.Equal(cause, ex.InnerException);
        }
    }
}