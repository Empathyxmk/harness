using System;
using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Original
{
    public class OldForwardInterProceduralAnalysisTest
    {
        [Fact]
        public void TestBasicConstructor()
        {
            var pr = new ProgramRepresentationStub();
            var ana = new OldForwardInterProceduralAnalysis<object, string, int>(pr, null)
            {
                ApplyImpl = (node, input) => input
            };
            Assert.NotNull(ana);
        }

        private class ProgramRepresentationStub : IProgramRepresentation
        {
            public object GetStartNode() => "start";
            public object GetExitNode() => "exit";
            public IEnumerable<object> GetPreds(object n) => new HashSet<object>();
            public IEnumerable<object> GetSuccs(object n) => new HashSet<object>();
            public IEnumerable<object> GetAllNodes() => new[] { "start" };
            public object GetOwner(object n) => "owner";
        }

        // Dummy abstract analysis class so we can override Apply in test
        private class OldForwardInterProceduralAnalysis<TNode, TMethod, TFact> :
            Vasco.OldForwardInterProceduralAnalysis<TNode, TMethod, TFact>
        {
            public Func<TNode, HashSet<TFact>, HashSet<TFact>> ApplyImpl { get; set; }

            public OldForwardInterProceduralAnalysis(IProgramRepresentation pr, object context)
                : base(pr, context) { }

            protected override HashSet<TFact> Apply(TNode node, HashSet<TFact> input) =>
                ApplyImpl(node, input);
        }
    }
}