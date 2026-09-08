using Xunit;
using ActivityFragmentMVP;

namespace ActivityFragmentMVP.Tests.Original
{
    public class AppModuleTest
    {
        [Fact]
        public void provideApplication_ReturnsApp()
        {
            App app = new App();
            AppModule module = new AppModule(app);
            var returned = module.provideApplication();
            Assert.Equal(app, returned);
        }
    }
}