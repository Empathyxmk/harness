using Xunit;
using yacy_yacy_grid_crawler.coverage;
using System;

namespace yacy_yacy_grid_crawler.tests.original
{
    public class DemoCoverageTests
    {
        [Fact]
        public void TestAdd_PositiveNumbers()
        {
            var demo = new DemoCoverage();
            Assert.Equal(5, demo.add(2, 3));
        }

        [Fact]
        public void TestAdd_NegativeNumbers()
        {
            var demo = new DemoCoverage();
            Assert.Equal(-5, demo.add(-2, -3));
        }

        [Fact]
        public void TestIsEven_EvenNumber()
        {
            var demo = new DemoCoverage();
            Assert.True(demo.isEven(4));
        }

        [Fact]
        public void TestIsEven_OddNumber()
        {
            var demo = new DemoCoverage();
            Assert.False(demo.isEven(5));
        }

        [Fact]
        public void TestDivide_RegularCase()
        {
            var demo = new DemoCoverage();
            Assert.Equal(2, demo.divide(6, 3));
        }

        [Fact]
        public void TestDivide_DivideByZero()
        {
            var demo = new DemoCoverage();
            var ex = Assert.Throws<DivideByZeroException>(() => demo.divide(10, 0));
            // .NET message usually is "Attempted to divide by zero."
            Assert.Contains("divide by zero", ex.Message.ToLowerInvariant());
        }
    }
}