using System;
using Xunit;
using Djilk.ROSBridgeClient;

namespace Djilk.ROSBridgeClient.Tests.Original
{
    public class CalculatorTests
    {
        [Fact]
        public void TestAdd()
        {
            var calc = new Calculator();
            Assert.Equal(5, calc.Add(2, 3));
        }

        [Fact]
        public void TestSubtract()
        {
            var calc = new Calculator();
            Assert.Equal(2, calc.Subtract(5, 3));
        }

        [Fact]
        public void TestMultiply()
        {
            var calc = new Calculator();
            Assert.Equal(6, calc.Multiply(2, 3));
        }

        [Fact]
        public void TestDivide()
        {
            var calc = new Calculator();
            Assert.Equal(2, calc.Divide(6, 3));
        }

        [Fact]
        public void TestDivideByZero()
        {
            var calc = new Calculator();
            Assert.Throws<ArgumentException>(() => calc.Divide(6, 0));
        }
    }
}