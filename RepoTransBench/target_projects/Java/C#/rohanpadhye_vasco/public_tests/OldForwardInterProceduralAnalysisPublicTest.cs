using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Public
{
    public class OldForwardInterProceduralAnalysisPublicTest
    {
        [Fact]
        public void TestDifferentConstructor()
        {
            var pr = new ProgramRepresentationStub();
            var ana = new OldForwardInterProceduralAnalysis<object, string, double>(pr, null)
            {
                ApplyImpl = (node, input) => input
            };
            Assert.NotNull(ana);
        }

        private class ProgramRepresentationStub : IProgramRepresentation
        {
            public object GetStartNode() => "alpha";
            public object GetExitNode() => "omega";
            public IEnumerable<object> GetPreds(object n) => new HashSet<object>();
            public IEnumerable<object> GetSuccs(object n) => new HashSet<object>();
            public IEnumerable<object> GetAllNodes() => new[] { "alpha" };
            public object GetOwner(object n) => "publicOwner";
        }

        private class OldForwardInterProceduralAnalysis<TNode, TMethod, TFact> :
            Vasco.OldForwardInterProceduralAnalysis<TNode, TMethod, TFact>
        {
            public System.Func<TNode, HashSet<TFact>, HashSet<TFact>> ApplyImpl { get; set; }
            public OldForwardInterProceduralAnalysis(IProgramRepresentation pr, object ctx) : base(pr, ctx) { }
            protected override HashSet<TFact> Apply(TNode node, HashSet<TFact> input) => ApplyImpl(node, input);
        }
    }
}