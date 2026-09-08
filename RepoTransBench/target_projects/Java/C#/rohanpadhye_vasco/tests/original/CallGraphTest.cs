using Xunit;

namespace Vasco.Tests.Original
{
    public class CallGraphTest
    {
        [Fact]
        public void BasicCoverage()
        {
            var cg = new CallGraph<string>();
            cg.AddEdge("A", "B");
            cg.AddEdge("A", "C");
            cg.AddEdge("B", "D");

            Assert.Contains("B", cg.GetCallees("A"));
            Assert.Contains("C", cg.GetCallees("A"));
            Assert.Equal(2, cg.GetCallees("A").Count);
            Assert.Contains("A", cg.GetCallers("B"));
            Assert.DoesNotContain("B", cg.GetCallees("C"));
        }
    }
}