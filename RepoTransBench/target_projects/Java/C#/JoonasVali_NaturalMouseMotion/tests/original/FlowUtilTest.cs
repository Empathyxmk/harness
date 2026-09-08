using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Util;

namespace JoonasVali.NaturalMouseMotion.Tests.Original
{
    public class FlowUtilTest
    {
        [Fact]
        public void ShouldSumFlows()
        {
            double[] flows = { 1.0, 2.0, 3.0 };
            double sum = FlowUtil.Sum(flows);
            Assert.Equal(6.0, sum);
        }
    }
}