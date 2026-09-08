using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Original
{
    public class DataFlowSolutionTest
    {
        [Fact]
        public void TestSetAndGet()
        {
            var dfs = new DataFlowSolution<string, int>();
            dfs.Set("A", new HashSet<int> { 42 });
            Assert.Contains(42, dfs.Get("A"));
            Assert.Contains("A", dfs.KeySet());
        }

        [Fact]
        public void TestMerge()
        {
            var dfs1 = new DataFlowSolution<string, int>();
            var dfs2 = new DataFlowSolution<string, int>();
            dfs1.Set("A", new HashSet<int> { 1 });
            dfs2.Set("A", new HashSet<int> { 2 });
            dfs1.Merge(dfs2);
            Assert.Contains(1, dfs1.Get("A"));
            Assert.Contains(2, dfs1.Get("A"));
        }

        [Fact]
        public void TestToString()
        {
            var dfs = new DataFlowSolution<string, int>();
            dfs.Set("B", new HashSet<int> { 100 });
            string str = dfs.ToString();
            Assert.Contains("B", str);
        }
    }
}