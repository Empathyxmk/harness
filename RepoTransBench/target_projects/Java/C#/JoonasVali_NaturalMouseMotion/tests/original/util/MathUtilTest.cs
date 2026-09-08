using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Util;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.Util
{
    public class MathUtilTest
    {
        [Theory]
        [InlineData(1, 2, 1)]
        [InlineData(2, 1, 1)]
        [InlineData(-1, -5, -5)]
        [InlineData(5, 5, 5)]
        public void TestMin(double a, double b, double expected)
        {
            Assert.Equal(expected, MathUtil.Min(a, b));
        }

        [Theory]
        [InlineData(1, 2, 2)]
        [InlineData(2, 1, 2)]
        [InlineData(-1, -5, -1)]
        [InlineData(5, 5, 5)]
        public void TestMax(double a, double b, double expected)
        {
            Assert.Equal(expected, MathUtil.Max(a, b));
        }

        [Theory]
        [InlineData(0, 0, 0, 0)]
        [InlineData(1, 2, 3, 2)]
        [InlineData(-1, 0, 1, 0)]
        public void TestMedian(double a, double b, double c, double expected)
        {
            Assert.Equal(expected, MathUtil.Median(a, b, c));
        }

        [Theory]
        [InlineData(3, 4, 5)]
        [InlineData(6, 8, 10)]
        [InlineData(0, 0, 0)]
        public void TestHypot(double a, double b, double expected)
        {
            Assert.Equal(expected, MathUtil.Hypot(a, b), 10);
        }
    }
}