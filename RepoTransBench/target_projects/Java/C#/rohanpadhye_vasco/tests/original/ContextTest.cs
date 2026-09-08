using Xunit;

namespace Vasco.Tests.Original
{
    public class ContextTest
    {
        [Fact]
        public void TestContextEquals()
        {
            var c1 = new Context("A", 1);
            var c2 = new Context("A", 1);
            var c3 = new Context("B", 2);

            Assert.Equal(c1, c2);
            Assert.NotEqual(c1, c3);
        }

        [Fact]
        public void TestContextHashCode()
        {
            var c1 = new Context("A", 1);
            var c2 = new Context("A", 1);
            Assert.Equal(c1.GetHashCode(), c2.GetHashCode());
        }

        [Fact]
        public void TestNullContext()
        {
            var c1 = new Context(null, 0);
            var c2 = new Context(null, 0);
            Assert.Equal(c1, c2);
        }

        [Fact]
        public void TestContextToString()
        {
            var c1 = new Context("Method", 5);
            Assert.Contains("Method", c1.ToString());
        }
    }
}