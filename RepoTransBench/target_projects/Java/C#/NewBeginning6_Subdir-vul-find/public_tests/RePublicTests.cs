using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class RePublicTests
    {
        [Fact]
        public void TestEscapeAndPattern()
        {
            var input = "x.y$^";
            var escaped = Re.Escape(input);
            Assert.NotNull(escaped);

            var pattern = @"\d+";
            Assert.True(Re.Pattern(pattern, "2024"));
            Assert.False(Re.Pattern(pattern, "test"));
            Assert.False(Re.Pattern("abc.*", "xyz"));
        }

        [Fact]
        public void TestContains()
        {
            Assert.True(Re.Contains("Goodbye moon", "moon"));
            Assert.False(Re.Contains("Goodbye", "sun"));
            Assert.False(Re.Contains(null, "def"));
            Assert.False(Re.Contains("def", null));
            Assert.False(Re.Contains(null, null));
        }
    }
}