using Xunit;
using Spring5Webapp;

namespace Spring5Webapp.Tests.Original
{
    public class Spring5webappApplicationTests
    {
        [Fact]
        public void ContextLoads()
        {
            Spring5webappApplication.Main(new string[] { });
        }
    }
}