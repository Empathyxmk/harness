using Xunit;

namespace ComponentDemo.Tests.Original
{
    public class ExampleInstrumentedTest_Share
    {
        [Fact]
        public void UseAppContext()
        {
            var appContext = new { PackageName = "com.loong.share" };
            Assert.Equal("com.loong.share", appContext.PackageName);
        }
    }
}