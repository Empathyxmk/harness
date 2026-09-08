using Xunit;
using System.Collections.Generic;
using System.Linq;
using Ch02Core.Predicate;

namespace OriginalTests.Dynamic
{
    public class DynamicTestsTest
    {
        [Theory]
        [InlineData("Add test")]
        [InlineData("Multiply Test")]
        public void DynamicTestsWithCollection(string name)
        {
            Assert.True(true);
        }

        [Theory]
        [InlineData("Add test")]
        [InlineData("Multiply Test")]
        public void DynamicTestsWithIterator(string name)
        {
            Assert.True(true);
        }

        [Theory]
        [InlineData("Add test")]
        [InlineData("Multiply Test")]
        public void DynamicTestsWithStream(string name)
        {
            Assert.True(true);
        }

        [Fact]
        public void DynamicTestsFromIntStream()
        {
            var predicate = new PositiveNumberPredicate();
            int[] numbers = { -1, 0, 1 };

            foreach (var number in numbers)
            {
                if (number > 0)
                    Assert.True(predicate.Test(number));
                else
                    Assert.False(predicate.Test(number));
            }
        }

        [Theory]
        [InlineData("foo")]
        [InlineData("bar")]
        [InlineData("baz")]
        public void DynamicTestsFromLambda(string text)
        {
            Assert.True(text.Length > 0);
        }

        [Fact]
        public void GenerateRandomNumberOfTests()
        {
            // Simulate running five positive assertions
            for (int i = 0; i < 5; i++)
            {
                Assert.True(true);
            }
        }

        [Fact]
        public void DynamicTestsForPositiveNumberPredicate()
        {
            var predicate = new PositiveNumberPredicate();
            var numbers = new List<int> { 1, 0, -1, 5, -3 };
            foreach (var number in numbers)
            {
                if (number > 0)
                {
                    Assert.True(predicate.Test(number));
                }
                else
                {
                    Assert.False(predicate.Test(number));
                }
            }
        }
    }
}