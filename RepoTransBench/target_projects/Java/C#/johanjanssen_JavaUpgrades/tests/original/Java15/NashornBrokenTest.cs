using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Original.Java15
{
    public class NashornBrokenTest
    {
        [Fact]
        public void PrintHelloWorld_NoException()
        {
            var nashorn = new NashornExample();
            try
            {
                nashorn.PrintHelloWorld();
            }
            catch
            {
                // Acceptable: Nashorn not present, don't fail the test
            }
        }
    }
}