using System;
using Xunit;

namespace GoogleAuth.Tests
{
    public class GoogleAuthenticatorExceptionTest
    {
        [Fact]
        public void TestExceptionMessage()
        {
            var ex = new GoogleAuthenticatorException("A message");
            Assert.Equal("A message", ex.Message);
        }

        [Fact]
        public void TestExceptionCause()
        {
            var cause = new Exception("root");
            var ex = new GoogleAuthenticatorException("A message", cause);
            Assert.Equal("A message", ex.Message);
            Assert.Equal(cause, ex.InnerException);
        }
    }
}