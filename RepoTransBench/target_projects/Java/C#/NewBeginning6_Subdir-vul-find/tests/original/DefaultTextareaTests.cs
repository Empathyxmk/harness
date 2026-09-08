using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.Tests.Original
{
    public class DefaultTextareaTests
    {
        [Fact]
        public void TestGetDefault()
        {
            var val = DefaultTextarea.GetDefault();
            Assert.NotNull(val);
            Assert.False(string.IsNullOrEmpty(val));
        }
    }
}