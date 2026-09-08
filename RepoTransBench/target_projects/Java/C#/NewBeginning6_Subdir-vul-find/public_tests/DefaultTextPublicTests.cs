using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class DefaultTextPublicTests
    {
        [Fact]
        public void TestGetDefault()
        {
            var text = DefaultText.GetDefault();
            Assert.NotNull(text);
            Assert.True(text.Contains("text") || text.Length > 10);
        }
    }
}