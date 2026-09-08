using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.Tests.Original
{
    public class MainSmokeTests
    {
        [Fact]
        public void TestMain()
        {
            string[] args = { };
            Main.Main(args);
        }
    }
}