using Xunit;

namespace PublicTests.Library
{
    // Simulates Android's ApplicationTestCase (library)
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