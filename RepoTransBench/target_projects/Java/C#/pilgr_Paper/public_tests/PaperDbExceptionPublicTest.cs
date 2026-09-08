using System;
using Xunit;

namespace PilgrPaper.PublicTests
{
    public class PaperDbExceptionPublicTest
    {
        [Fact]
        public void TestMessageConstructorPublic()
        {
            var ex = new PaperDbException("fail-public");
            Assert.Equal("fail-public", ex.Message);
        }

        [Fact]
        public void TestMessageAndThrowableConstructorPublic()
        {
            var t = new Exception("public-cause");
            var ex = new PaperDbException("fail-public2", t);
            Assert.Equal("fail-public2", ex.Message);
            Assert.Equal(t, ex.InnerException);
        }
    }
}