using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Public
{
    public class AsyncDaoExceptionPublicTests
    {
        [Fact]
        public void TestMessage()
        {
            var ex = new AsyncDaoException("testPublicMsg");
            Assert.Equal("testPublicMsg", ex.Message);
        }
    }
}