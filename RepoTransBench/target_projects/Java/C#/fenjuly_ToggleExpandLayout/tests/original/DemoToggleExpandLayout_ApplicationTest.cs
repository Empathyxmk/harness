using Xunit;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Original
{
    // Translation of demo/src/androidTest/java/com/fenjuly/toggleexpandlayout/ApplicationTest.java
    public class DemoToggleExpandLayout_ApplicationTest
    {
        [Fact]
        public void Application_Construction_DoesNotThrow()
        {
            var app = new Application();
            Assert.NotNull(app);
        }
    }
}