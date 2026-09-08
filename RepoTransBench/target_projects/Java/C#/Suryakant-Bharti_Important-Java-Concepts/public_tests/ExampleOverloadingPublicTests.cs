using Xunit;

namespace SuryakantBhartiImportantJavaConcepts.PublicTests
{
    public class ExampleOverloadingPublicTests
    {
        [Fact]
        public void TestMinFunctionInt()
        {
            Assert.Equal(2, ExampleOverloading.MinFunction(5, 2));
            Assert.Equal(-7, ExampleOverloading.MinFunction(-7, 9));
            Assert.Equal(-20, ExampleOverloading.MinFunction(-15, -20));
            Assert.Equal(0, ExampleOverloading.MinFunction(0, 0));
        }

        [Fact]
        public void TestMinFunctionDouble()
        {
            Assert.Equal(3.2, ExampleOverloading.MinFunction(8.7, 3.2), 9);
            Assert.Equal(-9.8, ExampleOverloading.MinFunction(-9.8, 4.5), 9);
            Assert.Equal(-11.3, ExampleOverloading.MinFunction(-11.3, -6.5), 9);
            Assert.Equal(-7.7, ExampleOverloading.MinFunction(-7.7, -7.7), 9);
        }
    }
}