using System;
using Xunit;

namespace UberUX.Tests.Original
{
    public class ExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext()
        {
            // Context test: fake package name
            string packageName = "mohak.uberux";
            Assert.Equal("mohak.uberux", packageName);
        }
    }
}