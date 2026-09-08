using Xunit;
using GBByPass;

namespace Tests.Original
{
    public class MainBranchCoverageTest
    {
        [Fact]
        public void TestReverseIfNotBlank_nullInput()
        {
            Assert.Null(Main.ReverseIfNotBlank(null));
        }

        [Fact]
        public void TestIsAllDigits_nullInput()
        {
            Assert.False(Main.IsAllDigits(null));
        }
    }
}