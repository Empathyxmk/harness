using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Util;

namespace JoonasVali.NaturalMouseMotion.PublicTests
{
    public class FlowUtilPublicTest
    {
        [Fact]
        public void ShouldFindAverageFlow()
        {
            double[] flows = { 1.0, 2.0, 3.0, 4.0, 5.0 };
            double avg = FlowUtil.Average(flows);
            Assert.Equal(3.0, avg);
        }
    }
}