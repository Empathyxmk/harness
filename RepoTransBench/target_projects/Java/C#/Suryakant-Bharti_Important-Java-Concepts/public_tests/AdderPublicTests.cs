using Xunit;

namespace SuryakantBhartiImportantJavaConcepts.PublicTests
{
    public class AdderPublicTests
    {
        [Fact]
        public void TestAddInt()
        {
            Assert.Equal(17, Adder.Add(9, 8));
            Assert.Equal(25, Adder.Add(15, 10));
            Assert.Equal(-6, Adder.Add(-3, -3));
        }

        [Fact]
        public void TestAddDouble()
        {
            Assert.Equal(21.1, Adder.Add(9.5, 11.6), 9);
            Assert.Equal(0.0, Adder.Add(-7.7, 7.7), 9);
            Assert.Equal(-6.6, Adder.Add(-2.2, -4.4), 9);
        }
    }
}