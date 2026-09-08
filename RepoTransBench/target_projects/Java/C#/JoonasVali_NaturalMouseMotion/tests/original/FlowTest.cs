using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Support;

namespace JoonasVali.NaturalMouseMotion.Tests.Original
{
    public class FlowTest
    {
        [Fact]
        public void ShouldGenerateDefaultFlow()
        {
            var flow = Flow.CreateDefault();
            Assert.NotNull(flow);
            Assert.True(flow.IsValid);
        }
    }
}