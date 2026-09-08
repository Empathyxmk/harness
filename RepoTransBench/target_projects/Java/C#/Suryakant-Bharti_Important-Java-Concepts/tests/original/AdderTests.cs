using Xunit;

namespace SuryakantBhartiImportantJavaConcepts.Tests
{
    public class AdderTests
    {
        [Fact]
        public void TestAddInt()
        {
            Assert.Equal(22, Adder.Add(11, 11));
            Assert.Equal(-8, Adder.Add(-10, 2));
            Assert.Equal(0, Adder.Add(0, 0));
        }

        [Fact]
        public void TestAddDouble()
        {
            Assert.Equal(24.9, Adder.Add(12.3, 12.6), 9);
            Assert.Equal(-4.4, Adder.Add(-2.2, -2.2), 9);
            Assert.Equal(0.0, Adder.Add(0.0, 0.0), 9);
        }
    }
}