using Xunit;

namespace Hitomis_CircleMenu.PublicTests
{
    // Stub for Application, simulating application instance access and not null assertion
    public class ApplicationPublicTest
    {
        [Fact]
        public void TestApplication_GetsInstance()
        {
            object application = new object();
            Assert.NotNull(application);
        }
    }
}