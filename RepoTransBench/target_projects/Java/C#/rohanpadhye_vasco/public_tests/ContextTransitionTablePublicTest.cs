using Xunit;

namespace Vasco.Tests.Public
{
    public class ContextTransitionTablePublicTest
    {
        [Fact]
        public void TestDifferentTransitionTable()
        {
            var table = new ContextTransitionTable<string, int, double>();
            var baseContext = new Context<string, int, double>("foo", 123);
            var next = new Context<string, int, double>("bar", 321);
            table.Put(baseContext, "edge", next);

            Assert.True(table.ContainsTransition(baseContext, "edge"));
            Assert.False(table.ContainsTransition(baseContext, "nonexistent"));
            Assert.Equal(next, table.GetTarget(baseContext, "edge"));
            Assert.Null(table.GetTarget(baseContext, "noTransition"));
        }

        [Fact]
        public void TestNullBaseContextTable()
        {
            var table = new ContextTransitionTable<string, int, double>();
            var baseContext = new Context<string, int, double>(null, -1);
            var next = new Context<string, int, double>("baz", 888);
            table.Put(baseContext, "x", next);

            Assert.True(table.ContainsTransition(baseContext, "x"));
            Assert.Equal(next, table.GetTarget(baseContext, "x"));
        }
    }
}