using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Public
{
    public class InterProceduralAnalysisPublicTest
    {
        [Fact]
        public void TrivialAnalysisPublicTest()
        {
            var pr = new ProgramRepresentationStub();
            var analysis = new ForwardInterProceduralAnalysisImpl(pr, null)
            {
                ApplyImpl = (node, input) => input
            };
            Assert.NotNull(analysis);
        }

        private class ProgramRepresentationStub : IProgramRepresentation
        {
            public object GetStartNode() => "begin";
            public object GetExitNode() => "end";
            public IEnumerable<object> GetPreds(object n) => null;
            public IEnumerable<object> GetSuccs(object n) => null;
            public IEnumerable<object> GetAllNodes() => null;
            public object GetOwner(object n) => null;
        }

        private class ForwardInterProceduralAnalysisImpl :
            Vasco.ForwardInterProceduralAnalysis<object, string, double>
        {
            public System.Func<object, HashSet<double>, HashSet<double>> ApplyImpl { get; set; }
            public ForwardInterProceduralAnalysisImpl(IProgramRepresentation pr, object ctx) : base(pr, ctx) { }
            protected override HashSet<double> Apply(object node, HashSet<double> input)
                => ApplyImpl(node, input);
        }
    }
}