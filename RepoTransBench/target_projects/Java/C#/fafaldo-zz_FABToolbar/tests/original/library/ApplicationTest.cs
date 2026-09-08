using Xunit;

namespace Tests.Original.Library
{
    // Simulates Android's ApplicationTestCase
    public class ApplicationTest
    {
        [Fact]
        public void ApplicationTest_CanConstruct()
        {
            var app = new object();
            Assert.NotNull(app);
        }
    }
}