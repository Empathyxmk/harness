using Xunit;
using Spring5Webapp;

namespace Spring5Webapp.Tests.Original
{
    public class Spring5webappApplicationMainMethodTests
    {
        [Fact]
        public void MainMethodRunsWithoutException()
        {
            Spring5webappApplication.Main(new string[] { });
        }
    }
}