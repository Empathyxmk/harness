using System;
using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.Tests.Original
{
    public class ReTests
    {
        [Fact]
        public void TestEscapeAndPattern()
        {
            var input = "a+b*c";
            var escaped = Re.Escape(input);
            Assert.NotNull(escaped);

            var pattern = "[a-z]+";
            Assert.True(Re.Pattern(pattern, "hello"));
            Assert.False(Re.Pattern(pattern, "123"));
            Assert.False(Re.Pattern(".*", ""));
        }

        [Fact]
        public void TestContains()
        {
            Assert.True(Re.Contains("Hello world", "world"));
            Assert.False(Re.Contains("Hello", "bye"));
            Assert.False(Re.Contains(null, "abc"));
            Assert.False(Re.Contains("abc", null));
            Assert.False(Re.Contains(null, null));
        }
    }
}