using Xunit;

namespace Vasco.Tests.Public
{
    public class ContextPublicTest
    {
        [Fact]
        public void TestContextEqualsDifferent()
        {
            var c1 = new Context("X", 9);
            var c2 = new Context("X", 9);
            var c3 = new Context("Y", 20);

            Assert.Equal(c1, c2);
            Assert.NotEqual(c1, c3);
        }

        [Fact]
        public void TestContextHashCodeDifferent()
        {
            var c1 = new Context("X", 9);
            var c2 = new Context("X", 9);
            Assert.Equal(c1.GetHashCode(), c2.GetHashCode());
        }

        [Fact]
        public void TestNullContextDifferent()
        {
            var c1 = new Context(null, 42);
            var c2 = new Context(null, 42);
            Assert.Equal(c1, c2);
        }

        [Fact]
        public void TestContextToStringDifferent()
        {
            var c1 = new Context("DifferentMethod", 99);
            Assert.Contains("DifferentMethod", c1.ToString());
        }
    }
}