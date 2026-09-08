using Xunit;

namespace OriginalTests
{
    public class ExceptionTest
    {
        [Fact]
        public void TestConnectionExceptionThrow()
        {
            Assert.Throws<ProjectName.ConnectionException>(() =>
            {
                throw new ProjectName.ConnectionException("Connection error");
            });
        }

        [Fact]
        public void TestNoFindHandlerExceptionThrow()
        {
            Assert.Throws<ProjectName.NoFindHandlerException>(() =>
            {
                throw new ProjectName.NoFindHandlerException("No handler found");
            });
        }
    }
}