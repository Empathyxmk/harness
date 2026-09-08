using Xunit;
using ActivityFragmentMVP;

namespace ActivityFragmentMVP.Tests.Original
{
    public class ModulesTest
    {
        [Fact]
        public void list_returnsNonNull()
        {
            App app = new App();
            object[] modules = Modules.list(app);
            Assert.NotNull(modules);
            Assert.True(modules.Length > 0);
            Assert.IsType<AppModule>(modules[0]);
        }
    }
}