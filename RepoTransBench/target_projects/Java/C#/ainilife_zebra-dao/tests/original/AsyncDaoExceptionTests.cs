using Xunit;
using Ainilife.ZebraDao;

namespace Ainilife.ZebraDao.Tests.Original
{
    public class AsyncDaoExceptionTests
    {
        [Fact]
        public void TestMessage()
        {
            var ex = new AsyncDaoException("msg");
            Assert.Equal("msg", ex.Message);
        }
    }
}