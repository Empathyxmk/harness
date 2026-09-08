using System;
using System.Collections.Generic;
using Xunit;
using BmwcaritHmmLib;

namespace PublicTests
{
    public class UtilsPublicTest
    {
        [Fact]
        public void TestNormalizeProbabilitiesDifferent()
        {
            var probs = new Dictionary<string, double>
            {
                { "orange", 4.0 },
                { "banana", 6.0 }
            };

            var norm = Utils.NormalizeProbabilities(probs);

            Assert.Equal(0.4, norm["orange"], 10);
            Assert.Equal(0.6, norm["banana"], 10);

            // Original input is not modified
            Assert.Equal(4.0, probs["orange"], 10);
            Assert.Equal(6.0, probs["banana"], 10);
        }

        [Fact]
        public void TestNormalizeEmptyDifferent()
        {
            Assert.Throws<ArgumentException>(() => Utils.NormalizeProbabilities(new Dictionary<string, double>()));
        }

        [Fact]
        public void TestNormalizeNullValueDifferent()
        {
            var p = new Dictionary<string, double?> { { "something", null } };
            Assert.Throws<NullReferenceException>(() =>
            {
                Utils.NormalizeProbabilitiesNullValue(p);
            });
        }

        [Fact]
        public void TestSumDifferentValues()
        {
            var l = new List<double> { 2.5, 3.0, 7.5 };
            Assert.Equal(13.0, Utils.Sum(l), 10);
        }

        [Fact]
        public void TestLog2DifferentInputs()
        {
            Assert.Equal(1.0, Utils.Log2(2.0), 10);
            Assert.Equal(2.0, Utils.Log2(4.0), 10);
            Assert.Equal(0.0, Utils.Log2(1.0), 10);
        }

        [Fact]
        public void TestLog2ZeroDifferent()
        {
            Assert.Throws<ArgumentException>(() => Utils.Log2(0.0));
        }

        [Fact]
        public void TestLog2NegativeDifferent()
        {
            Assert.Throws<ArgumentException>(() => Utils.Log2(-2.0));
        }

        [Fact]
        public void TestLogSumExpListDifferent()
        {
            var d = new List<double> { Math.Log(2.0), Math.Log(10.0) };
            double expected = Math.Log(2.0 + 10.0);
            Assert.Equal(expected, Utils.LogSumExp(d), 10);
        }

        [Fact]
        public void TestLogSumExpArrayDifferent()
        {
            double[] arr = { Math.Log(5), Math.Log(3) };
            double expected = Math.Log(5.0 + 3.0);
            Assert.Equal(expected, Utils.LogSumExp(arr), 10);
        }
    }
}