using Xunit;
using GBByPass;

namespace PublicTests
{
    public class RandomUtilBranchCoveragePublicTest
    {
        [Fact]
        public void TestRandomString_lengthTwo()
        {
            string s = RandomUtil.RandomString(2);
            Assert.NotNull(s);
            Assert.Equal(2, s.Length);
            Assert.Matches("^[A-Za-z0-9]{2}$", s);
        }

        [Fact]
        public void TestRandomString_mediumLength()
        {
            string s = RandomUtil.RandomString(50);
            Assert.NotNull(s);
            Assert.Equal(50, s.Length);
            Assert.Matches("^[A-Za-z0-9]{50}$", s);
        }
    }
}