using Xunit;

namespace ComponentDemo.Tests.Original
{
    public class ExampleInstrumentedTest_Base
    {
        [Fact]
        public void UseAppContext()
        {
            var appContext = new { PackageName = "com.loong.base.test" };
            Assert.Equal("com.loong.base.test", appContext.PackageName);
        }
    }
}