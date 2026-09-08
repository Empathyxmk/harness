using System.Collections.Generic;
using Xunit;

namespace Vasco.Tests.Original
{
    public class ContextTransitionTableTestExtra
    {
        [Fact]
        public void TestPutAndGetContextTransition()
        {
            var table = new ContextTransitionTable<int, string>();
            table.Put("foo", 1, 2);
            table.Put("foo", 1, 3);
            Assert.Contains(2, table.Get("foo", 1));
            Assert.Contains(3, table.Get("foo", 1));
        }

        [Fact]
        public void TestEmpty()
        {
            var table = new ContextTransitionTable<int, string>();
            Assert.Empty(table.Get("bar", 42));
        }
    }
}