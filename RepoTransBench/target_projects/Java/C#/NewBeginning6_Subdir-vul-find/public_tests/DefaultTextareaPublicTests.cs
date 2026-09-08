using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class DefaultTextareaPublicTests
    {
        [Fact]
        public void TestGetDefault()
        {
            var val = DefaultTextarea.GetDefault();
            Assert.NotNull(val);
            Assert.True(val.Trim().Length > 0);
        }
    }
}