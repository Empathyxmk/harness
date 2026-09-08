using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Support;

namespace JoonasVali.NaturalMouseMotion.PublicTests
{
    public class FlowPublicTest
    {
        [Fact]
        public void ShouldInstantiateFlow()
        {
            var flow = new Flow();
            Assert.NotNull(flow);
        }
    }
}