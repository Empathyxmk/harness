using System;
using Xunit;
using Djilk.ROSBridgeClient;

namespace Djilk.ROSBridgeClient.Tests.Public
{
    public class CalculatorPublicTests
    {
        [Fact]
        public void TestAdd()
        {
            var calc = new Calculator();
            // Changed input from (2,3)=5 to (4,7)=11
            Assert.Equal(11, calc.Add(4, 7));
        }

        [Fact]
        public void TestSubtract()
        {
            var calc = new Calculator();
            // Changed input from (5,3)=2 to (10,4)=6
            Assert.Equal(6, calc.Subtract(10, 4));
        }

        [Fact]
        public void TestMultiply()
        {
            var calc = new Calculator();
            // Changed input from (2,3)=6 to (5,4)=20
            Assert.Equal(20, calc.Multiply(5, 4));
        }

        [Fact]
        public void TestDivide()
        {
            var calc = new Calculator();
            // Changed input from (6,3)=2 to (20,4)=5
            Assert.Equal(5, calc.Divide(20, 4));
        }

        [Fact]
        public void TestDivideByZero()
        {
            var calc = new Calculator();
            // Test still checks divide by zero, but use a different numerator value (original 6, now 17)
            Assert.Throws<ArgumentException>(() => calc.Divide(17, 0));
        }
    }
}