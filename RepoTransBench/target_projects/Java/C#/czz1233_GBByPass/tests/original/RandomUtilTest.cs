using Xunit;
using GBByPass;

namespace Tests.Original
{
    public class RandomUtilTest
    {
        [Fact]
        public void TestRandomString_Length()
        {
            Assert.Equal(8, RandomUtil.RandomString(8).Length);
            Assert.Equal(1, RandomUtil.RandomString(1).Length);
            Assert.Equal(32, RandomUtil.RandomString(32).Length);
        }

        [Fact]
        public void TestRandomString_Characters()
        {
            string str = RandomUtil.RandomString(100);
            Assert.Matches("^[A-Za-z0-9]{100}$", str);
        }

        [Fact]
        public void TestRandomString_ZeroAndNegativeLength()
        {
            Assert.Equal("", RandomUtil.RandomString(0));
            Assert.Equal("", RandomUtil.RandomString(-5));
        }
    }
}