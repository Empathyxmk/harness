using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.PublicTests
{
    public class PairPublicTest
    {
        [Fact]
        public void TestOfAndGetters_Public()
        {
            var pair = Pair.Of(12345, "hello");
            Assert.Equal(12345, pair.First);
            Assert.Equal("hello", pair.Second);

            var pair2 = Pair.Of(3.14, 2.71);
            Assert.Equal(3.14, pair2.First);
            Assert.Equal(2.71, pair2.Second);
        }

        [Fact]
        public void TestEqualsAndHashCode_Public()
        {
            var a = Pair.Of("A", "B");
            var b = Pair.Of("A", "B");
            Assert.Equal(a, b);
            Assert.Equal(a.GetHashCode(), b.GetHashCode());

            var c = Pair.Of("A", "C");
            Assert.NotEqual(a, c);

            var d = Pair.Of<string, string>(null, "B");
            var e = Pair.Of<string, string>(null, "B");
            Assert.Equal(d, e);
            Assert.Equal(d.GetHashCode(), e.GetHashCode());
        }
    }
}