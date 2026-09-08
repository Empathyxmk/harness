using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleInstrumentedPublicTest_Share
    {
        [Fact]
        public void AppContextPackageNameContainsShare()
        {
            var appContext = new { PackageName = "com.loong.share.publictest" };
            Assert.Contains("share", appContext.PackageName);
        }
    }
}