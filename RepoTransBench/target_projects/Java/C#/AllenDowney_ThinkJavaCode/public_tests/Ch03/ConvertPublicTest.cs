using Xunit;
using AllenDowney.ThinkJavaCode;

namespace PublicTests.Ch03
{
    public class ConvertPublicTest
    {
        [Fact]
        public void TestCelsiusToFahrenheitPublicData()
        {
            Assert.Equal(32.0, Convert.CelsiusToFahrenheit(0), 2);
            Assert.Equal(122.0, Convert.CelsiusToFahrenheit(50), 2);
            Assert.Equal(68.0, Convert.CelsiusToFahrenheit(20), 2);
            Assert.Equal(98.6, Convert.CelsiusToFahrenheit(37), 2);
        }

        [Fact]
        public void TestFahrenheitToCelsiusPublicData()
        {
            Assert.Equal(0.0, Convert.FahrenheitToCelsius(32), 2);
            Assert.Equal(100.0, Convert.FahrenheitToCelsius(212), 2);
            Assert.Equal(40.0, Convert.FahrenheitToCelsius(104), 2);
            Assert.Equal(5.0, Convert.FahrenheitToCelsius(41), 2);
        }
    }
}