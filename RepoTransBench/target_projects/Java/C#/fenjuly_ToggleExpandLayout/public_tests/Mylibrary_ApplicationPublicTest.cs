using Xunit;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Public
{
    // Translation of library/src/androidTest/java/com/fenjuly/mylibrary/ApplicationPublicTest.java
    public class Mylibrary_ApplicationPublicTest
    {
        [Fact]
        public void Application_Construction_DoesNotThrow_Public()
        {
            var app = new Application();
            Assert.NotNull(app);
        }
    }
}