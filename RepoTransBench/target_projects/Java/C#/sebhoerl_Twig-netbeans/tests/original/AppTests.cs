using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class AppTests
    {
        [Fact]
        public void TestMainNoException()
        {
            // No exception should be thrown from main
            App.Main(new string[] { });
        }

        [Fact]
        public void TestAppBasic()
        {
            var app = new App();
            Assert.NotNull(app);
        }
    }
}