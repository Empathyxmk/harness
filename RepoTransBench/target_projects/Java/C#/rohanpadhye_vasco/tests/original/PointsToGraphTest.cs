using Xunit;

namespace Vasco.Tests.Original
{
    public class PointsToGraphTest
    {
        [Fact]
        public void TestBasicUsage()
        {
            var ptg = new PointsToGraph<string, string>();
            ptg.Add("a", "x");
            ptg.Add("a", "y");
            ptg.Add("b", "z");

            Assert.Contains("x", ptg.Get("a"));
            Assert.Contains("y", ptg.Get("a"));
            Assert.Contains("z", ptg.Get("b"));
            Assert.DoesNotContain("z", ptg.Get("a"));
        }

        [Fact]
        public void TestMerge()
        {
            var g1 = new PointsToGraph<string, string>();
            var g2 = new PointsToGraph<string, string>();
            g1.Add("A", "one");
            g2.Add("A", "two");
            g1.Merge(g2);
            Assert.Contains("one", g1.Get("A"));
            Assert.Contains("two", g1.Get("A"));
        }
    }
}