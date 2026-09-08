using Xunit;
using ActivityFragmentMVP;

namespace ActivityFragmentMVP.Tests.Public
{
    public class AppModulePublicTest
    {
        [Fact]
        public void provideApplication_DifferentAppInstance()
        {
            App anotherApp = new App();
            AppModule module = new AppModule(anotherApp);
            var returned = module.provideApplication();
            Assert.Same(anotherApp, returned);
        }
    }
}