using System;
using System.Collections.Generic;
using Xunit;
using BmwcaritHmmLib;

namespace OriginalTests
{
    public class UtilsTest
    {
        [Fact]
        public void TestInitialHashMapCapacity()
        {
            Assert.Equal(14, Utils.InitialHashMapCapacity(10));
        }

        [Fact]
        public void TestLogToNonLogProbabilities()
        {
            var logProbs = new Dictionary<string, double>
            {
                { "A", Math.Log(0.4) },
                { "B", Math.Log(0.6) }
            };
            var probs = Utils.LogToNonLogProbabilities(logProbs);
            Assert.Equal(0.4, probs["A"], 10);
            Assert.Equal(0.6, probs["B"], 10);
        }

        [Fact]
        public void TestProbabilityInRange()
        {
            Assert.True(Utils.ProbabilityInRange(1.0, 1e-8));
            Assert.True(Utils.ProbabilityInRange(0.0, 1e-8));
            Assert.False(Utils.ProbabilityInRange(-0.01, 1e-4));
            Assert.True(Utils.ProbabilityInRange(1.000009, 1e-3));
            Assert.False(Utils.ProbabilityInRange(1.2, 1e-4));
        }
    }
}