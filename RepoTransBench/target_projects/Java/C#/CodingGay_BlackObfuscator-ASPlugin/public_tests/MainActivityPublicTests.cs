using Xunit;
using BlackObfuscatorASPlugin;

namespace BlackObfuscatorASPlugin.PublicTests
{
    public class MainActivityPublicTests
    {
        [Fact]
        public void TestGetWelcomeMessageWithDifferentUser()
        {
            Assert.Equal("Welcome, Charlie!", MainActivity.GetWelcomeMessage("Charlie"));
            Assert.Equal("Welcome, Zoe!", MainActivity.GetWelcomeMessage("Zoe"));
        }
    }
}