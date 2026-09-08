using Xunit;
using GBByPass;

namespace PublicTests
{
    public class RandomUtilFullPublicTest
    {
        [Fact]
        public void TestRandomString_negativeLength()
        {
            string val = RandomUtil.RandomString(-7);
            Assert.Equal("", val);
        }

        [Fact]
        public void TestRandomString_allValidCharactersMany()
        {
            string val = RandomUtil.RandomString(32);
            Assert.NotNull(val);
            Assert.Equal(32, val.Length);
            Assert.Matches("^[A-Za-z0-9]{32}$", val);
        }
    }
}