using Xunit;
using YacyGridSearch;

namespace YacyGridSearch.Tests.Public
{
    public class DummyLogicPublicTest
    {
        [Fact]
        public void TestAddDifferentNumbers()
        {
            var d = new DummyLogic();
            Assert.Equal(15, d.Add(8, 7));
            Assert.Equal(-5, d.Add(-2, -3));
            Assert.Equal(5, d.Add(15, -10));
            Assert.Equal(0, d.Add(10, -10));
            Assert.Equal(0, d.Add(-8, 8));
            Assert.Equal(14, d.Add(10, 4));
        }

        [Fact]
        public void TestIsPositiveDifferent()
        {
            var d = new DummyLogic();
            Assert.True(d.IsPositive(1));
            Assert.False(d.IsPositive(-1));
            Assert.False(d.IsPositive(0));
        }

        [Fact]
        public void TestDescribeDifferentData()
        {
            var d = new DummyLogic();
            Assert.Equal("equal", d.Describe(-3, -3));
            Assert.Equal("greater", d.Describe(12, 5));
            Assert.Equal("less", d.Describe(-10, 0));
        }
    }
}