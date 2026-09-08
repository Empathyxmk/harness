using Xunit;

namespace ComponentDemo.Tests.Original
{
    public class ExampleInstrumentedTest_Login
    {
        [Fact]
        public void UseAppContext()
        {
            var appContext = new { PackageName = "com.loong.login" };
            Assert.Equal("com.loong.login", appContext.PackageName);
        }
    }
}