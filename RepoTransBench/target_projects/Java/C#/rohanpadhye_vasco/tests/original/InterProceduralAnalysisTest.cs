using Xunit;

namespace Vasco.Tests.Original
{
    public class InterProceduralAnalysisTest
    {
        [Fact]
        public void TrivialAnalysisTest()
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
            public object GetStartNode() => "start";
            public object GetExitNode() => "exit";
            public System.Collections.IEnumerable GetPreds(object n) => null;
            public System.Collections.IEnumerable GetSuccs(object n) => null;
            public System.Collections.IEnumerable GetAllNodes() => null;
            public object GetOwner(object n) => null;
        }

        private class ForwardInterProceduralAnalysisImpl : Vasco.ForwardInterProceduralAnalysis<object, string, int>
        {
            public System.Func<object, System.Collections.Generic.HashSet<int>, System.Collections.Generic.HashSet<int>> ApplyImpl { get; set; }
            public ForwardInterProceduralAnalysisImpl(IProgramRepresentation pr, object context) : base(pr, context) { }
            protected override System.Collections.Generic.HashSet<int> Apply(object node, System.Collections.Generic.HashSet<int> input)
            {
                return ApplyImpl(node, input);
            }
        }
    }
}