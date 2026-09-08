using Xunit;

namespace OriginalTests.CloudGateway
{
    // Suite class to mirror Java's @RunWith(JUnitPlatform.class).
    // In xUnit, all tests are discoverable automatically.
    // Here for structural parity.
    public class CloudGatewayApplicationTestSuite
    {
        [Fact]
        public void TestSuiteCoversApplicationAndController()
        {
            // Instantiate both test classes to ensure they are part of the suite.
            // In xUnit, all test classes/methods are run automatically. No further logic needed.
        }
    }
}