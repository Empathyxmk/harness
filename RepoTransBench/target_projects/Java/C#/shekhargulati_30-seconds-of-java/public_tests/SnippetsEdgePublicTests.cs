using Xunit;
using SnippetsLib;
using System.Linq;

namespace SnippetsPublicTests
{
    public class SnippetsEdgePublicTests
    {
        [Fact]
        public void Gcd_with_array_of_zeros_is_zero()
        {
            Assert.Equal(0, Snippets.Gcd(new int[] { 0, 0, 0 }));
        }

        [Fact]
        public void Lcm_with_single_element_array_is_value_itself()
        {
            Assert.Equal(99, Snippets.Lcm(new int[] { 99 }));
        }

        [Fact]
        public void ArrayMax_with_negative_numbers_returns_max()
        {
            Assert.Equal(-2, Snippets.ArrayMax(new int[] { -9, -2, -17 }));
        }

        [Fact]
        public void ArrayMin_with_all_equal_numbers_returns_that_number()
        {
            Assert.Equal(7, Snippets.ArrayMin(new int[] { 7, 7, 7 }));
        }

        [Fact]
        public void Chunk_empty_array_returns_empty_result()
        {
            var chunks = Snippets.Chunk(new int[] { }, 5);
            Assert.Empty(chunks);
        }

        [Fact]
        public void CountOccurrences_no_matching_values_returns_zero()
        {
            Assert.Equal(0, Snippets.CountOccurrences(new int[] { 8, 9, 10 }, 5));
        }

        [Fact]
        public void DeepFlatten_empty_array_returns_empty_array()
        {
            var flatten = Snippets.DeepFlatten(new object[] { });
            Assert.Empty(flatten);
        }

        [Fact]
        public void Difference_with_first_array_empty_returns_empty()
        {
            var difference = Snippets.Difference(new int[] { }, new int[] { 2, 3 });
            Assert.Empty(difference);
        }

        [Fact]
        public void Difference_with_second_array_empty_returns_first_array()
        {
            var difference = Snippets.Difference(new int[] { 4, 5, 6 }, new int[] { });
            Assert.True(new int[] { 4, 5, 6 }.SequenceEqual(difference));
        }
        // Additional edge public tests can be added as needed.
    }
}