using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.Tests
{
    public class PairTest
    {
        [Fact]
        public void TestOfGetters()
        {
            var pair = Pair.Of("hello", 42);
            Assert.Equal("hello", pair.First);
            Assert.Equal(42, pair.Second);
        }

        [Fact]
        public void TestEqualsHashCode_SameObject()
        {
            var pair = Pair.Of("foo", 123);
            Assert.True(pair.Equals(pair));
            Assert.Equal(pair.GetHashCode(), pair.GetHashCode());
        }

        [Fact]
        public void TestEqualsHashCode_EqualPairs()
        {
            var pair1 = Pair.Of("a", 1);
            var pair2 = Pair.Of("a", 1);
            Assert.True(pair1.Equals(pair2));
            Assert.True(pair2.Equals(pair1));
            Assert.Equal(pair1.GetHashCode(), pair2.GetHashCode());
        }

        [Fact]
        public void TestEquals_NotEqualByFirst()
        {
            var pair1 = Pair.Of("a", 1);
            var pair2 = Pair.Of("b", 1);
            Assert.False(pair1.Equals(pair2));
            Assert.False(pair2.Equals(pair1));
        }

        [Fact]
        public void TestEquals_NotEqualBySecond()
        {
            var pair1 = Pair.Of("a", 1);
            var pair2 = Pair.Of("a", 2);
            Assert.False(pair1.Equals(pair2));
            Assert.False(pair2.Equals(pair1));
        }

        [Fact]
        public void TestEquals_NullObject()
        {
            var pair = Pair.Of("x", 10);
            Assert.False(pair.Equals(null));
        }

        [Fact]
        public void TestEquals_DifferentClass()
        {
            var pair = Pair.Of("x", 10);
            Assert.False(pair.Equals((object)"not a pair"));
        }

        [Fact]
        public void TestEquals_NullFields()
        {
            var p1 = Pair.Of<string, int?>(null, null);
            var p2 = Pair.Of<string, int?>(null, null);
            Assert.True(p1.Equals(p2));
            Assert.Equal(p1.GetHashCode(), p2.GetHashCode());
        }

        [Fact]
        public void TestEquals_NullFirstDifferentSecond()
        {
            var p1 = Pair.Of<string, int?> (null, 10);
            var p2 = Pair.Of<string, int?> (null, 11);
            Assert.False(p1.Equals(p2));
        }

        [Fact]
        public void TestEquals_DifferentFirstNullSecond()
        {
            var p1 = Pair.Of("x", (int?)null);
            var p2 = Pair.Of("y", (int?)null);
            Assert.False(p1.Equals(p2));
        }

        [Fact]
        public void TestEquals_NullFirstNonNullOther()
        {
            var p1 = Pair.Of<string, int?>(null, 1);
            var p2 = Pair.Of("z", 1);
            Assert.False(p1.Equals(p2));
        }

        [Fact]
        public void TestEquals_NonNullFirstNullOther()
        {
            var p1 = Pair.Of("z", 1);
            var p2 = Pair.Of<string, int?>(null, 1);
            Assert.False(p1.Equals(p2));
        }
    }
}