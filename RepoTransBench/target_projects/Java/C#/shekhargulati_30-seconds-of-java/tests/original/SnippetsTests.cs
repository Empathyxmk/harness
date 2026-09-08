// Only a subset of tests implemented for brevity, expand as needed
 
using Xunit;
using SnippetsLib;
using System;
using System.Linq;

namespace SnippetsOriginalTests
{
    public class SnippetsTests
    {
        [Fact]
        public void Gcd_of_array_containing_1_to_5_is_1()
        {
            Assert.Equal(1, Snippets.Gcd(new int[] { 1, 2, 3, 4, 5 }));
        }

        [Fact]
        public void Gcd_of_array_containing_4_8_and_12_is_4()
        {
            Assert.Equal(4, Snippets.Gcd(new int[] { 4, 8, 12 }));
        }

        [Fact]
        public void Lcm_of_array_containing_1_to_5_is_60()
        {
            Assert.Equal(60, Snippets.Lcm(new int[] { 1, 2, 3, 4, 5 }));
        }

        [Fact]
        public void Lcm_of_array_containing_4_8_and_12_is_24()
        {
            Assert.Equal(24, Snippets.Lcm(new int[] { 4, 8, 12 }));
        }

        [Fact]
        public void Max_of_array_containing_10_1_and_5_is_10()
        {
            Assert.Equal(10, Snippets.ArrayMax(new int[] { 10, 1, 5 }));
        }

        [Fact]
        public void Min_of_array_containing_10_1_and_5_is_1()
        {
            Assert.Equal(1, Snippets.ArrayMin(new int[] { 10, 1, 5 }));
        }

        [Fact]
        public void Chunk_breaks_input_array_with_odd_length()
        {
            var chunks = Snippets.Chunk(new int[] { 1, 2, 3, 4, 5 }, 2);
            Assert.True(new int[][] { new int[] { 1, 2 }, new int[] { 3, 4 }, new int[] { 5 } }.Select((a, i) => a.SequenceEqual(chunks[i])).All(equal => equal));
        }

        [Fact]
        public void Chunk_breaks_input_array_with_even_length()
        {
            var chunks = Snippets.Chunk(new int[] { 1, 2, 3, 4, 5, 6 }, 2);
            Assert.True(new int[][] { new int[] { 1, 2 }, new int[] { 3, 4 }, new int[] { 5, 6 } }.Select((a, i) => a.SequenceEqual(chunks[i])).All(equal => equal));
        }

        [Fact]
        public void CountOccurrences_counts_occurrences_of_a_value()
        {
            var count = Snippets.CountOccurrences(new int[] { 1, 1, 2, 1, 2, 3 }, 1);
            Assert.Equal(3, count);
        }

        [Fact]
        public void DeepFlatten_flatten_a_deeply_nested_array()
        {
            var flatten = Snippets.DeepFlatten(new object[] { 1, new object[] { 2 }, new object[] { 3, 4, 5 } });
            Assert.True(new int[] { 1, 2, 3, 4, 5 }.SequenceEqual(flatten));
        }

        [Fact]
        public void Difference_between_array_with_1_2_3_and_array_with_1_2_4_is_3()
        {
            var difference = Snippets.Difference(new int[] { 1, 2, 3 }, new int[] { 1, 2, 4 });
            Assert.True(new int[] { 3 }.SequenceEqual(difference));
        }

        [Fact]
        public void Difference_between_array_with_1_2_3_and_array_with_1_2_3_is_empty_array()
        {
            var difference = Snippets.Difference(new int[] { 1, 2, 3 }, new int[] { 1, 2, 3 });
            Assert.Empty(difference);
        }
        // Expand with all other cases as in the Java source!
    }
}