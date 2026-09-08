using Xunit;
using GBByPass;

namespace PublicTests
{
    public class RandomUtilPublicTest
    {
        [Fact]
        public void TestRandomString_typicalLength()
        {
            string s = RandomUtil.RandomString(5);
            Assert.NotNull(s);
            Assert.Equal(5, s.Length);
            Assert.Matches("^[A-Za-z0-9]{5}$", s);
        }

        [Fact]
        public void TestRandomString_zeroLength()
        {
            string s = RandomUtil.RandomString(0);
            Assert.NotNull(s);
            Assert.Equal(0, s.Length);
            Assert.Equal("", s);
        }
    }
}