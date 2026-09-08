using Xunit;

namespace ComponentDemo.Tests.Original
{
    public class ExampleInstrumentedTest_ComponentDemo
    {
        [Fact]
        public void UseAppContext()
        {
            var appContext = new { PackageName = "com.loong.componentdemo" };
            Assert.Equal("com.loong.componentdemo", appContext.PackageName);
        }
    }
}