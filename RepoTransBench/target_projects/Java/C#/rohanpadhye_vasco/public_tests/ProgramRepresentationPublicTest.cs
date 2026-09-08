using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Public
{
    public class ProgramRepresentationPublicTest
    {
        [Fact]
        public void TestProgramRepresentationDifferentNodes()
        {
            var pr = new ProgramRepresentationStub();
            Assert.Equal("publicStart", pr.GetStartNode());
            Assert.Equal("publicExit", pr.GetExitNode());
            Assert.Equal("ownerZ", pr.GetOwner("publicStart"));
            Assert.True(pr.GetPreds("publicExit").GetEnumerator().MoveNext());
            Assert.True(pr.GetSuccs("publicStart").GetEnumerator().MoveNext());
        }

        [Fact]
        public void TestNullIterables()
        {
            var pr = new ProgramRepresentationNullStub();
            Assert.Equal("begin", pr.GetStartNode());
            Assert.Equal("finish", pr.GetExitNode());
            Assert.Null(pr.GetOwner("whatever"));
        }

        private class ProgramRepresentationStub : IProgramRepresentation
        {
            public object GetStartNode() => "publicStart";
            public object GetExitNode() => "publicExit";
            public IEnumerable<object> GetPreds(object n) => new[] { "predX" };
            public IEnumerable<object> GetSuccs(object n) => new[] { "succY" };
            public IEnumerable<object> GetAllNodes() => new[] { "publicStart", "publicExit" };
            public object GetOwner(object n) => "ownerZ";
        }

        private class ProgramRepresentationNullStub : IProgramRepresentation
        {
            public object GetStartNode() => "begin";
            public object GetExitNode() => "finish";
            public IEnumerable<object> GetPreds(object n) => null;
            public IEnumerable<object> GetSuccs(object n) => null;
            public IEnumerable<object> GetAllNodes() => null;
            public object GetOwner(object n) => null;
        }
    }
}