using Xunit;
using GBByPass;

namespace PublicTests
{
    public class MainFullCoveragePublicTest
    {
        [Fact]
        public void TestReverseIfNotBlank_withNumbersAndLetters()
        {
            Assert.Equal("Ba98", Main.ReverseIfNotBlank("89aB"));
        }

        [Fact]
        public void TestReverseIfNotBlank_withSpecialCharacters()
        {
            Assert.Equal("!@#", Main.ReverseIfNotBlank("#@!"));
        }

        [Fact]
        public void TestIsAllDigits_withSpacesAndDigits()
        {
            Assert.False(Main.IsAllDigits(" 789 "));
        }

        [Fact]
        public void TestIsAllDigits_withDash()
        {
            Assert.False(Main.IsAllDigits("123-456"));
        }
    }
}