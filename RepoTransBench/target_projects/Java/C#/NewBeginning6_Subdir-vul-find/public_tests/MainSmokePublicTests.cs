using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class MainSmokePublicTests
    {
        [Fact]
        public void TestMainLaunch()
        {
            // Pass some random args to make sure Main.main does not throw
            try
            {
                string[] args = { "hello", "world", "--flag" };
                Main.Main(args);
            }
            catch (System.Exception e)
            {
                Assert.True(false, "Main.Main() threw exception: " + e);
            }
        }
    }
}