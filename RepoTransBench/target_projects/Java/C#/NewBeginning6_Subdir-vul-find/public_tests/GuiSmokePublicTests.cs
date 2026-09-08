using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class GuiSmokePublicTests
    {
        [Fact]
        public void TestBasicGuiInstantiation()
        {
            try
            {
                var gui = new Gui();
                Assert.NotNull(gui);
            }
            catch (System.Exception e)
            {
                Assert.True(false, "Gui instantiation failed: " + e);
            }
        }
    }
}