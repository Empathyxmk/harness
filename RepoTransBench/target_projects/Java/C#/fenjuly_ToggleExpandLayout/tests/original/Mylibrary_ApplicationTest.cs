using Xunit;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Original
{
    // Translation of library/src/androidTest/java/com/fenjuly/mylibrary/ApplicationTest.java
    public class Mylibrary_ApplicationTest
    {
        [Fact]
        public void Application_Construction_DoesNotThrow()
        {
            var app = new Application();
            Assert.NotNull(app);
        }
    }
}