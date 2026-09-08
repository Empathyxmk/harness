using Xunit;
using GBByPass;

namespace Tests.Original
{
    public class RandomUtilFullTest
    {
        [Fact]
        public void TestRandomStringWithZeroLength()
        {
            string result = RandomUtil.RandomString(0);
            Assert.NotNull(result);
            Assert.Equal(0, result.Length);
        }

        [Fact]
        public void TestRandomStringWithNegativeLength()
        {
            string result = RandomUtil.RandomString(-1);
            Assert.NotNull(result);
            Assert.Equal(0, result.Length);
        }

        [Fact]
        public void TestRandomStringWithHighLength()
        {
            string result = RandomUtil.RandomString(100);
            Assert.NotNull(result);
            Assert.Equal(100, result.Length);
        }

        [Fact]
        public void TestRandomStringIsAlphanumeric()
        {
            string result = RandomUtil.RandomString(20);
            Assert.True(System.Text.RegularExpressions.Regex.IsMatch(result, "^[A-Za-z0-9]+$") || result.Length == 0);
        }
        // The following methods are commented out in Java; omitted in C# for fidelity
    }
}