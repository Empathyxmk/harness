using Xunit;
using Ch02Core.Predicate;

namespace OriginalTests.Predicate
{
    public class PositiveNumberPredicateTest
    {
        private PositiveNumberPredicate _predicate;

        public PositiveNumberPredicateTest()
        {
            _predicate = new PositiveNumberPredicate();
        }

        [Fact]
        public void TestWithPositiveNumber()
        {
            Assert.True(_predicate.Test(10));
        }

        [Fact]
        public void TestWithZero()
        {
            Assert.False(_predicate.Test(0));
        }

        [Fact]
        public void TestWithNegativeNumber()
        {
            Assert.False(_predicate.Test(-5));
        }
    }
}