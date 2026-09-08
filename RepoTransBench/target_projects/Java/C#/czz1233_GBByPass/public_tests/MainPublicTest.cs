using Xunit;
using GBByPass;

namespace PublicTests
{
    public class MainPublicTest
    {
        [Fact]
        public void TestReverseIfNotBlank_nonBlank()
        {
            Assert.Equal("edcba", Main.ReverseIfNotBlank("abcde"));
            Assert.Equal("Z", Main.ReverseIfNotBlank("Z"));
        }

        [Fact]
        public void TestReverseIfNotBlank_blank()
        {
            Assert.Equal("\t", Main.ReverseIfNotBlank("\t"));
            Assert.Equal("    ", Main.ReverseIfNotBlank("    "));
        }

        [Fact]
        public void TestIsAllDigits_numeric()
        {
            Assert.True(Main.IsAllDigits("987654"));
        }

        [Fact]
        public void TestIsAllDigits_nonNumeric()
        {
            Assert.False(Main.IsAllDigits("def"));
            Assert.False(Main.IsAllDigits("789ghi"));
            Assert.False(Main.IsAllDigits(""));
            Assert.False(Main.IsAllDigits("    "));
        }

        [Fact]
        public void TestMain_withArgs()
        {
            Main.MainEntry(new string[] { "456" });
            Main.MainEntry(new string[] { "def" });
            Main.MainEntry(new string[] { " " });
        }
    }
}