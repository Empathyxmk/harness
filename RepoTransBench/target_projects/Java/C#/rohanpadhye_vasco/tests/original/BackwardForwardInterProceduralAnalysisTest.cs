using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Original
{
    public class BackwardForwardInterProceduralAnalysisTest
    {
        [Fact]
        public void CoverageForAbstract()
        {
            var pr = new ProgramRepresentationStub();
            var ana = new BackwardInterProceduralAnalysisStub(pr, null)
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

        private class BackwardInterProceduralAnalysisStub :
            Vasco.BackwardInterProceduralAnalysis<object, string, int>
        {
            public System.Func<object, HashSet<int>, HashSet<int>> ApplyImpl { get; set; }
            public BackwardInterProceduralAnalysisStub(IProgramRepresentation pr, object context) : base(pr, context) { }
            protected override HashSet<int> Apply(object node, HashSet<int> input)
            {
                return ApplyImpl(node, input);
            }
        }
    }
}