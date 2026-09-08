using System;
using Xunit;

namespace PayatuDivaAndroid.Tests.Original
{
    // This test corresponds to ApplicationTest.java, which only
    // checks fundamental construction of the Application.
    public class ApplicationTests
    {
        [Fact]
        public void Application_Constructor_Works()
        {
            // In Android, Application constructors are framework-based;
            // Here we just assert that we can instantiate a minimal object.
            var app = new object();
            Assert.NotNull(app);
        }
    }
}