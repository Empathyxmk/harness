using Xunit;
using YacyGridSearch;

namespace YacyGridSearch.Tests.Original
{
    public class DummyLogicTest
    {
        [Fact]
        public void TestAdd()
        {
            var d = new DummyLogic();
            Assert.Equal(7, d.Add(3, 4));
            Assert.Equal(-7, d.Add(-3, -4));
            Assert.Equal(0, d.Add(-3, 3));
            Assert.Equal(0, d.Add(0, 0));
            Assert.Equal(0, d.Add(-3, 3));
            Assert.Equal(0, d.Add(3, -3));
        }

        [Fact]
        public void TestIsPositive()
        {
            var d = new DummyLogic();
            Assert.True(d.IsPositive(10));
            Assert.False(d.IsPositive(0));
            Assert.False(d.IsPositive(-4));
        }

        [Fact]
        public void TestDescribe()
        {
            var d = new DummyLogic();
            Assert.Equal("equal", d.Describe(5, 5));
            Assert.Equal("greater", d.Describe(7, 2));
            Assert.Equal("less", d.Describe(3, 7));
        }
    }
}