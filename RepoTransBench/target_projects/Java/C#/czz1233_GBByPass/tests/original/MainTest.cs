using Xunit;
using GBByPass;

namespace Tests.Original
{
    public class MainTest
    {
        [Fact]
        public void TestReverseIfNotBlank_nonBlank()
        {
            Assert.Equal("321", Main.ReverseIfNotBlank("123"));
            Assert.Equal("a", Main.ReverseIfNotBlank("a"));
        }

        [Fact]
        public void TestReverseIfNotBlank_blank()
        {
            Assert.Equal("", Main.ReverseIfNotBlank(""));
            Assert.Equal("   ", Main.ReverseIfNotBlank("   "));
        }

        [Fact]
        public void TestIsAllDigits_numeric()
        {
            Assert.True(Main.IsAllDigits("123456"));
        }

        [Fact]
        public void TestIsAllDigits_nonNumeric()
        {
            Assert.False(Main.IsAllDigits("abc"));
            Assert.False(Main.IsAllDigits("123abc"));
            Assert.False(Main.IsAllDigits(""));
            Assert.False(Main.IsAllDigits("   "));
        }

        [Fact]
        public void TestMain_withArgs()
        {
            // Coverage: doesn't assert output, just covers code path.
            Main.MainEntry(new string[] { "123" });
            Main.MainEntry(new string[] { "abc" });
            Main.MainEntry(new string[] { "" });
        }
    }
}