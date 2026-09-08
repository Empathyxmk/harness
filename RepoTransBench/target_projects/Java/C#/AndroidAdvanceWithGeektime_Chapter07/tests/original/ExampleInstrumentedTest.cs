using Xunit;

namespace TestsOriginal
{
    public class ExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext()
        {
            // Simulated equivalent: test passes if package name is as expected.
            var appContext = new AppContextSimulator("matrix.tencent.com.matrix_android");
            Assert.Equal("matrix.tencent.com.matrix_android", appContext.PackageName);
        }
    }

    // Simulated context (since there is no actual Android context in .NET)
    internal class AppContextSimulator
    {
        public string PackageName { get; }

        public AppContextSimulator(string packageName)
        {
            PackageName = packageName;
        }
    }
}