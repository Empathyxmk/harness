using Xunit;
using GBByPass;

namespace PublicTests
{
    public class MainBranchCoveragePublicTest
    {
        [Fact]
        public void TestReverseIfNotBlank_emptyStringInput()
        {
            Assert.Equal("", Main.ReverseIfNotBlank(""));
        }

        [Fact]
        public void TestIsAllDigits_emptyStringInput()
        {
            Assert.False(Main.IsAllDigits(""));
        }
    }
}