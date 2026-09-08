using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleInstrumentedPublicTest_Base
    {
        [Fact]
        public void PackageNameContainsBase()
        {
            var appContext = new { PackageName = "com.loong.base.publictest" };
            Assert.Contains("base", appContext.PackageName);
        }
    }
}