using System;
using Xunit;

namespace PilgrPaper.OriginalTests
{
    public class PaperDbExceptionTest
    {
        [Fact]
        public void TestMessageConstructor()
        {
            var ex = new PaperDbException("fail");
            Assert.Equal("fail", ex.Message);
        }

        [Fact]
        public void TestMessageAndThrowableConstructor()
        {
            var t = new Exception("t cause");
            var ex = new PaperDbException("fail2", t);
            Assert.Equal("fail2", ex.Message);
            Assert.Equal(t, ex.InnerException);
        }
    }
}