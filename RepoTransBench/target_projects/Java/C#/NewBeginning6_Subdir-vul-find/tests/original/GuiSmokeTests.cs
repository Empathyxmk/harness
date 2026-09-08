using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.Tests.Original
{
    public class GuiSmokeTests
    {
        [Fact]
        public void TestMain()
        {
            // Smoke test for coverage, won't actually render a window in CI
            string[] args = { "--help" };
            Gui.Main(args);
        }
    }
}