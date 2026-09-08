using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.Tests.Original
{
    public class DefaultTextTests
    {
        [Fact]
        public void TestGetDefault()
        {
            var val = DefaultText.GetDefault();
            Assert.NotNull(val);
            Assert.False(string.IsNullOrEmpty(val));
        }
    }
}