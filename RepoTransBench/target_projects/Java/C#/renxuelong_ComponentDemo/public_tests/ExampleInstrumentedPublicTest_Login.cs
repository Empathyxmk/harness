using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleInstrumentedPublicTest_Login
    {
        [Fact]
        public void GetAppContextPackageNameContainsLogin()
        {
            var appContext = new { PackageName = "com.loong.login.public" };
            Assert.Contains("login", appContext.PackageName);
        }
    }
}