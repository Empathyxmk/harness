using Xunit;
using InstallLion;
using System;

namespace InstallLion.Tests.Original
{
    public class CalculatorTests
    {
        private readonly Calculator calculator = new Calculator();

        [Fact]
        public void TestAdd()
        {
            Assert.Equal(5, calculator.Add(2, 3));
            Assert.Equal(-1, calculator.Add(2, -3));
        }

        [Fact]
        public void TestSubtract()
        {
            Assert.Equal(-1, calculator.Subtract(2, 3));
            Assert.Equal(5, calculator.Subtract(2, -3));
        }

        [Fact]
        public void TestMultiply()
        {
            Assert.Equal(6, calculator.Multiply(2, 3));
            Assert.Equal(-6, calculator.Multiply(2, -3));
        }

        [Fact]
        public void TestDivide()
        {
            Assert.Equal(2, calculator.Divide(6, 3));
            Assert.Equal(-2, calculator.Divide(6, -3));
        }

        [Fact]
        public void TestDivideByZero()
        {
            var ex = Assert.Throws<ArgumentException>(() => calculator.Divide(1, 0));
            Assert.Equal("Divider cannot be zero.", ex.Message);
        }
    }
}