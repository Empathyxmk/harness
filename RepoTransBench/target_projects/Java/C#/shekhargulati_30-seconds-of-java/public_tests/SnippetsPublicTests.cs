using Xunit;
using SnippetsLib;
using System.Linq;

namespace SnippetsPublicTests
{
    public class SnippetsPublicTests
    {
        [Fact]
        public void Gcd_of_array_containing_6_9_15_is_3()
        {
            Assert.Equal(3, Snippets.Gcd(new int[] { 6, 9, 15 }));
        }

        [Fact]
        public void Gcd_of_array_containing_14_28_56_is_14()
        {
            Assert.Equal(14, Snippets.Gcd(new int[] { 14, 28, 56 }));
        }

        [Fact]
        public void Lcm_of_array_containing_2_3_7_is_42()
        {
            Assert.Equal(42, Snippets.Lcm(new int[] { 2, 3, 7 }));
        }

        [Fact]
        public void Lcm_of_array_containing_5_10_20_is_20()
        {
            Assert.Equal(20, Snippets.Lcm(new int[] { 5, 10, 20 }));
        }

        [Fact]
        public void Max_of_array_containing_4_8_and_6_is_8()
        {
            Assert.Equal(8, Snippets.ArrayMax(new int[] { 4, 8, 6 }));
        }

        [Fact]
        public void Min_of_array_containing_17_8_and_25_is_8()
        {
            Assert.Equal(8, Snippets.ArrayMin(new int[] { 17, 8, 25 }));
        }

        [Fact]
        public void Chunk_breaks_input_array_with_size_3()
        {
            var chunks = Snippets.Chunk(new int[] { 10, 20, 30, 40, 50, 60, 70 }, 3);
            Assert.True(new int[][] { new int[] { 10, 20, 30 }, new int[] { 40, 50, 60 }, new int[] { 70 } }.Select((a, i) => a.SequenceEqual(chunks[i])).All(equal => equal));
        }

        [Fact]
        public void Chunk_breaks_input_array_evenly_with_size_4()
        {
            var chunks = Snippets.Chunk(new int[] { 2, 4, 6, 8, 10, 12, 14, 16 }, 4);
            Assert.True(new int[][] { new int[] { 2, 4, 6, 8 }, new int[] { 10, 12, 14, 16 } }.Select((a, i) => a.SequenceEqual(chunks[i])).All(equal => equal));
        }

        [Fact]
        public void CountOccurrences_counts_occurrences_of_value_5()
        {
            var count = Snippets.CountOccurrences(new int[] { 5, 3, 5, 2, 5, 6 }, 5);
            Assert.Equal(3, count);
        }

        [Fact]
        public void DeepFlatten_flattens_varied_nested_array()
        {
            var flatten = Snippets.DeepFlatten(new object[] { 7, new object[] { 8, new object[] { 9, 10 } }, 11 });
            Assert.True(new int[] { 7, 8, 9, 10, 11 }.SequenceEqual(flatten));
        }

        [Fact]
        public void Difference_between_array_9_8_7_and_7_8_5_is_9()
        {
            var difference = Snippets.Difference(new int[] { 9, 8, 7 }, new int[] { 7, 8, 5 });
            Assert.True(new int[] { 9 }.SequenceEqual(difference));
        }
    }
}