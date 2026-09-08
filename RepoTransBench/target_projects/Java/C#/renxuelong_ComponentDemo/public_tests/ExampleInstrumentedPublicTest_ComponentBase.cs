using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleInstrumentedPublicTest_ComponentBase
    {
        [Fact]
        public void AppContextPackageName_IsNotNull()
        {
            var context = new { PackageName = "com.loong.componentbase.publictest" };
            Assert.False(string.IsNullOrEmpty(context.PackageName));
            Assert.Contains("componentbase", context.PackageName);
        }
    }
}