using System;
using Xunit;

namespace XegerLib.Tests.Public
{
    public class XegerEdgePublicTest
    {
        [Fact]
        public void TestInvalidRegexThrowsException()
        {
            // Unclosed parenthesis instead (different from bracket)
            Assert.Throws<ArgumentException>(() =>
            {
                new Xeger("(abc", new Random());
            });
        }

        [Fact]
        public void TestGenerateMinEqualsMax()
        {
            var generator = new Xeger("[cd]{2,2}e", new Random(77));
            string s = generator.Generate(3, 3);
            Assert.Equal(3, s.Length);
            Assert.Matches(@"[cd]{2}e", s);
        }

        [Fact]
        public void TestGenerateTooShortThrowsException()
        {
            var generator = new Xeger("xyz", new Random(13));
            Assert.Throws<Xeger.FailedRandomWalkException>(() =>
            {
                generator.Generate(5, 5);
            });
        }

        [Fact]
        public void TestGenerateAcceptOnFirstStep()
        {
            var generator = new Xeger("b*", new Random(11));
            string s = generator.Generate(0, 0);
            Assert.Matches(@"b*", s);
            Assert.Equal(0, s.Length);
        }

        [Fact]
        public void TestGenerateNormalFlow()
        {
            var generator = new Xeger("abc|xyz", new Random(3));
            string s = generator.Generate();
            Assert.True(s == "abc" || s == "xyz");
        }
    }
}