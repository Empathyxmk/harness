using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Public
{
    public class DataFlowSolutionPublicTest
    {
        [Fact]
        public void TestDifferentInOutValues()
        {
            var inDict = new Dictionary<string, int> { { "A", 111 }, { "B", 222 } };
            var outDict = new Dictionary<string, int> { { "A", 777 }, { "B", 888 } };
            var dfs = new DataFlowSolution<string, int>(inDict, outDict);

            Assert.Equal(111, dfs.GetValueBefore("A"));
            Assert.Equal(222, dfs.GetValueBefore("B"));
            Assert.Equal(777, dfs.GetValueAfter("A"));
            Assert.Equal(888, dfs.GetValueAfter("B"));
        }

        [Fact]
        public void TestNullReturnFromMaps()
        {
            var inDict = new Dictionary<string, int>();
            var outDict = new Dictionary<string, int>();
            var dfs = new DataFlowSolution<string, int>(inDict, outDict);

            Assert.Null(dfs.GetValueBefore("notPresent"));
            Assert.Null(dfs.GetValueAfter("notPresent"));
        }
    }
}