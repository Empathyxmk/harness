using Xunit;
using Redwarp.NinePatchResizer.worker;

namespace Redwarp.NinePatchResizer.Tests.Original
{
    public class OutputTests
    {
        [Fact]
        public void TestEnumFormat()
        {
            Assert.Equal("png", Output.PNG.GetFormat());
            Assert.Equal("jpg", Output.JPG.GetFormat());
        }
    }
}