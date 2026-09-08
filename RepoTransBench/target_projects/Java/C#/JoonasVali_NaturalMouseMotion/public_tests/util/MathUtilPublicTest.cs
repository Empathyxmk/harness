using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Util;

namespace JoonasVali.NaturalMouseMotion.PublicTests.Util
{
    public class MathUtilPublicTest
    {
        [Theory]
        [InlineData(1, 1)]
        [InlineData(-5, 5)]
        [InlineData(0, 0)]
        public void TestAbs(double input, double expected)
        {
            Assert.Equal(expected, MathUtil.Abs(input));
        }

        [Theory]
        [InlineData(9, 3)]
        [InlineData(25, 5)]
        [InlineData(0, 0)]
        public void TestSqrt(double input, double expected)
        {
            Assert.Equal(expected, MathUtil.Sqrt(input));
        }
    }
}