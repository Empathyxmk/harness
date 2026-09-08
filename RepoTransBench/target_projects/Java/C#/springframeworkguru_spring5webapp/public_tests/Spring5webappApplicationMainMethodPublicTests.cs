using Xunit;
using Spring5Webapp;

namespace Spring5Webapp.PublicTests
{
    public class Spring5webappApplicationMainMethodPublicTests
    {
        [Fact]
        public void MainMethodRunsWithoutExceptionWithArgs()
        {
            Spring5webappApplication.Main(new string[] { "publicTestArg" });
        }
    }
}