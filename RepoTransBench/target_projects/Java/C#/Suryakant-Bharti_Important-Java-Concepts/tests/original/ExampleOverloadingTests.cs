using Xunit;

namespace SuryakantBhartiImportantJavaConcepts.Tests
{
    public class ExampleOverloadingTests
    {
        [Fact]
        public void TestMinFunctionInt()
        {
            Assert.Equal(6, ExampleOverloading.MinFunction(11, 6));
            Assert.Equal(-3, ExampleOverloading.MinFunction(-3, 4));
            Assert.Equal(-5, ExampleOverloading.MinFunction(-5, -2));
            Assert.Equal(7, ExampleOverloading.MinFunction(7, 7));
        }

        [Fact]
        public void TestMinFunctionDouble()
        {
            Assert.Equal(7.3, ExampleOverloading.MinFunction(7.3, 9.4), 9);
            Assert.Equal(-5.5, ExampleOverloading.MinFunction(-5.5, 0.0), 9);
            Assert.Equal(-10.2, ExampleOverloading.MinFunction(-10.2, -2.3), 9);
            Assert.Equal(12.0, ExampleOverloading.MinFunction(12.0, 12.0), 9);
        }
    }
}