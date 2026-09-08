using Xunit;

namespace PublicTests.App
{
    // Simulates Android's ApplicationTestCase
    public class ApplicationPublicTest
    {
        [Fact]
        public void ApplicationPublicTest_CanConstruct()
        {
            var app = new object();
            Assert.NotNull(app);
        }
    }
}