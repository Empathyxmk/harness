using Xunit;
using GBByPass;

namespace Tests.Original
{
    public class RandomUtilBranchCoverageTest
    {
        [Fact]
        public void TestRandomString_lengthOne()
        {
            string s = RandomUtil.RandomString(1);
            Assert.NotNull(s);
            Assert.Equal(1, s.Length);
            Assert.Matches("^[A-Za-z0-9]$", s);
        }

        [Fact]
        public void TestRandomString_largeLength()
        {
            string s = RandomUtil.RandomString(1000);
            Assert.NotNull(s);
            Assert.Equal(1000, s.Length);
            Assert.Matches("^[A-Za-z0-9]{1000}$", s);
        }
    }
}