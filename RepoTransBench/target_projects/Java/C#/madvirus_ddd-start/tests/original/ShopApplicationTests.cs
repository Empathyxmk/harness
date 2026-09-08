using Xunit;

namespace MadvirusDddStart.Tests.Original
{
    public class ShopApplicationTests
    {
        [Fact]
        public void MainRunsWithoutException()
        {
            // No exception should be thrown
            MadvirusDddStart.Program.Main(Array.Empty<string>());
        }
    }
}