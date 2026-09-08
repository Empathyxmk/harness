using Xunit;

namespace AndroidUtils.PublicTests
{
    public class ExampleInstrumentedPublicTest
    {
        [Fact]
        public void UseAppContext_Public()
        {
            var appContext = new AppContext("com.example.administrator.androidutils");
            Assert.NotEqual("com.example.anotherpackage", appContext.PackageName);
        }
    }

    public class AppContext
    {
        public string PackageName { get; private set; }
        public AppContext(string packageName)
        {
            PackageName = packageName;
        }
    }
}