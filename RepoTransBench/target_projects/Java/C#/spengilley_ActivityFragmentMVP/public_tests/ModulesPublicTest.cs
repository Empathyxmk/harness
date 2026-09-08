using Xunit;
using ActivityFragmentMVP;

namespace ActivityFragmentMVP.Tests.Public
{
    public class ModulesPublicTest
    {
        [Fact]
        public void list_nonNullDifferentAppInstance()
        {
            App testApp = new App();
            object[] modules = Modules.list(testApp);
            Assert.NotNull(modules);
            Assert.True(modules.Length > 0);
            Assert.IsType<AppModule>(modules[0]);
        }
    }
}