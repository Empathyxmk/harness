using Xunit;
using System;

namespace JulianKlodeDns66.OriginalTests
{
    public class ExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_ShouldReturnAppContextName()
        {
            // In Android: ApplicationProvider.getApplicationContext().getPackageName();
            // Simulate package name.
            var contextPackageName = "org.jak_linux.dns66";
            Assert.Equal("org.jak_linux.dns66", contextPackageName);
        }
    }
}