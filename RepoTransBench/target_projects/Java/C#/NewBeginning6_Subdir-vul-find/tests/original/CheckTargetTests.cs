using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.Tests.Original
{
    public class CheckTargetTests
    {
        [Fact]
        public void TestIsValid()
        {
            Assert.True(CheckTarget.IsValid("http://test.com"));
            Assert.False(CheckTarget.IsValid("invalid_string"));
            Assert.False(CheckTarget.IsValid(""));
        }

        [Fact]
        public void TestSanitize()
        {
            Assert.Equal("abc", CheckTarget.Sanitize("abc"));
            Assert.Equal("", CheckTarget.Sanitize(null));
        }
    }
}