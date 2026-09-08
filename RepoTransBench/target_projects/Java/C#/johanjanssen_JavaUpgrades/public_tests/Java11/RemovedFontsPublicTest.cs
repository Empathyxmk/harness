using Xunit;
using Johanjanssen.JavaUpgrades;
using System.Linq;
using System.Drawing.Text;

namespace Johanjanssen.JavaUpgrades.Tests.Public.Java11
{
    public class RemovedFontsPublicTest
    {
        [Fact]
        public void TestGetAvailableFontFamilyNames_Public()
        {
            var fontNames = FontExample.GetAvailableFontFamilyNames();
            Assert.NotNull(fontNames);

            bool found = fontNames.Contains("Monospaced") || fontNames.Contains("DialogInput");
            Assert.True(found, "Should have some basic monospace font family available");
        }
    }
}