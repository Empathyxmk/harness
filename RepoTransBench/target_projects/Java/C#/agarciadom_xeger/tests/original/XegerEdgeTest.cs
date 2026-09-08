using System;
using Xunit;

namespace XegerLib.Tests.Original
{
    public class XegerEdgeTest
    {
        [Fact]
        public void TestInvalidRegexThrowsException()
        {
            // Unclosed bracket
            Assert.Throws<ArgumentException>(() =>
            {
                new Xeger("[A-Z", new Random());
            });
        }

        [Fact]
        public void TestGenerateMinEqualsMax()
        {
            var generator = new Xeger("[ab]{3,3}c", new Random(42));
            string s = generator.Generate(4, 4);
            Assert.Equal(4, s.Length);
            Assert.Matches(@"[ab]{3}c", s);
        }

        [Fact]
        public void TestGenerateTooShortThrowsException()
        {
            var generator = new Xeger("abc", new Random(42));
            Assert.Throws<Xeger.FailedRandomWalkException>(() =>
            {
                // ask for longer than regex allows to force fail
                generator.Generate(4, 4);
            });
        }

        [Fact]
        public void TestGenerateAcceptOnFirstStep()
        {
            // Regex that can accept on empty string
            var generator = new Xeger("a*", new Random(42));
            string s = generator.Generate(0, 0);
            Assert.Matches(@"a*", s);
            Assert.Equal(0, s.Length);
        }

        [Fact]
        public void TestGenerateNormalFlow()
        {
            var generator = new Xeger("abc|def", new Random(1));
            string s = generator.Generate();
            Assert.True(s == "abc" || s == "def");
        }
    }
}