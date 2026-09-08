using Xunit;

namespace PublicTests
{
    public class ExampleInstrumentedPublicTest
    {
        [Fact]
        public void UseAppContextPublic()
        {
            var appContext = new AppContextSimulator("matrix.tencent.com.matrix_android");
            Assert.NotNull(appContext);
            Assert.NotEqual("com.geektime.systrace.dummy", appContext.PackageName);
        }
    }

    // Simulated context, public variant
    internal class AppContextSimulator
    {
        public string PackageName { get; }

        public AppContextSimulator(string packageName)
        {
            PackageName = packageName;
        }
    }
}