using Xunit;

namespace Vasco.Tests.Original
{
    public class CallGraphTransformerTest
    {
        [Fact]
        public void Coverage()
        {
            var cg = new CallGraph<string>();
            cg.AddEdge("A", "B");
            var t = new CallGraphTransformerStub();
            t.Transform(cg);
            Assert.Contains("C", cg.GetCallees("B"));
        }

        private class CallGraphTransformerStub : CallGraphTransformer<string>
        {
            public override void Transform(CallGraph<string> graph)
            {
                graph.AddEdge("B", "C");
            }
        }
    }
}