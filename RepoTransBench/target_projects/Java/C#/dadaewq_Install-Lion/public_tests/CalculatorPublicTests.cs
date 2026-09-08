using Xunit;
using InstallLion;
using System;

namespace InstallLion.PublicTests
{
    public class CalculatorPublicTests
    {
        private readonly Calculator calculator = new Calculator();

        [Fact]
        public void TestAdd()
        {
            Assert.Equal(11, calculator.Add(4, 7));
            Assert.Equal(3, calculator.Add(6, -3));
        }

        [Fact]
        public void TestSubtract()
        {
            Assert.Equal(8, calculator.Subtract(10, 2));
            Assert.Equal(12, calculator.Subtract(9, -3));
        }

        [Fact]
        public void TestMultiply()
        {
            Assert.Equal(35, calculator.Multiply(5, 7));
            Assert.Equal(-20, calculator.Multiply(4, -5));
        }

        [Fact]
        public void TestDivide()
        {
            Assert.Equal(9, calculator.Divide(72, 8));
            Assert.Equal(-4, calculator.Divide(12, -3));
        }

        [Fact]
        public void TestDivideByZero()
        {
            var ex = Assert.Throws<ArgumentException>(() => calculator.Divide(8, 0));
            Assert.Equal("Divider cannot be zero.", ex.Message);
        }
    }
}