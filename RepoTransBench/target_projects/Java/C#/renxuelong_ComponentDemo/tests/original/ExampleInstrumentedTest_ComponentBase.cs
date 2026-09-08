using Xunit;

namespace ComponentDemo.Tests.Original
{
    // Mock substitute for Android Context
    public class MockContext
    {
        public string PackageName { get; set; }
    }

    public class ExampleInstrumentedTest_ComponentBase
    {
        [Fact]
        public void UseAppContext()
        {
            var appContext = new MockContext { PackageName = "com.loong.componentbase.test" };
            Assert.Equal("com.loong.componentbase.test", appContext.PackageName);
        }
    }
}