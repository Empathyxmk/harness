using Xunit;
using Redwarp.NinePatchResizer.worker;

namespace Redwarp.NinePatchResizer.PublicTests
{
    public class OutputPublicTests
    {
        [Fact]
        public void TestEnumFormat()
        {
            Assert.True(Output.PNG.GetFormat().Equals("png", System.StringComparison.OrdinalIgnoreCase));
            Assert.True(Output.JPG.GetFormat().ToUpper() == "JPG");
        }
    }
}