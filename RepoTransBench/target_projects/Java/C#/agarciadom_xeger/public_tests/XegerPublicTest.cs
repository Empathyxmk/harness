using System;
using Xunit;

namespace XegerLib.Tests.Public
{
    public class XegerPublicTest
    {
        [Fact]
        public void TestLiteralGeneration()
        {
            string regex = "abcXYZ";
            var generator = new Xeger(regex);
            string result = generator.Generate();
            Assert.Equal("abcXYZ", result);
        }

        [Fact]
        public void TestSimpleDigitGeneration()
        {
            string regex = "[4-6]{4}";
            var generator = new Xeger(regex);
            string result = generator.Generate();
            Assert.Equal(4, result.Length);
            Assert.Matches(@"[4-6]{4}", result);
        }

        [Fact]
        public void TestSimpleAlphaGeneration()
        {
            string regex = "[A-C]{3}";
            var generator = new Xeger(regex);
            string result = generator.Generate();
            Assert.Equal(3, result.Length);
            Assert.Matches(@"[A-C]{3}", result);
        }

        [Fact]
        public void TestRangeWithSpecialChar()
        {
            string regex = "[M-Q]{2}-[7-9]{2}";
            var generator = new Xeger(regex);
            string str = generator.Generate();
            Assert.Matches(@"[M-Q]{2}-[7-9]{2}", str);
        }

        [Fact]
        public void TestRandomNumericGeneration()
        {
            // Choose a pattern and valid assertion that will always pass
            string regex = "[98]{8}";
            var generator = new Xeger(regex);
            string str = generator.Generate();
            Assert.Equal(8, str.Length);
            Assert.Matches(@"[98]{8}", str);
        }
    }
}