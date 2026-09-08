using Xunit;

namespace OriginalTests.ServiceRegistry
{
    public static class ServiceRegistryApplication
    {
        // Stand-in for the application's entry point
        public static void Main(string[]? args)
        {
            // No operation, just for line coverage.
        }
    }

    public class ServiceRegistryApplicationTestSuite
    {
        [Fact]
        public void TestMainMethod()
        {
            ServiceRegistryApplication.Main(new string[] { "--spring.profiles.active=test" });
        }

        [Fact]
        public void TestNoArgsMain()
        {
            ServiceRegistryApplication.Main(null);
        }
    }
}