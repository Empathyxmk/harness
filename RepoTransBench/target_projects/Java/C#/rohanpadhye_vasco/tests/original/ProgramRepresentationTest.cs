using Xunit;

namespace Vasco.Tests.Original
{
    public class ProgramRepresentationTest
    {
        [Fact]
        public void BasicOverrideTest()
        {
            var pr = new ProgramRepresentationStub();
            Assert.Equal("start", pr.GetStartNode());
            Assert.Equal("exit", pr.GetExitNode());
            Assert.Null(pr.GetPreds("x"));
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
    }
}