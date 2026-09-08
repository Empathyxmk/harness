using Xunit;
using Ch02Core.Repeated;
using System.Collections.Generic;

namespace OriginalTests.Repeated
{
    public class RepeatedTestsTest
    {
        private static HashSet<int> integerSet = new HashSet<int>();
        private static List<int> integerList = new List<int>();

        [Theory]
        [InlineData(1)]
        [InlineData(2)]
        [InlineData(3)]
        [InlineData(4)]
        [InlineData(5)]
        public void AddNumber(int repetition)
        {
            var calculator = new Calculator();
            int result = calculator.Add(1, 1);
            Assert.Equal(2, result);
        }

        [Theory]
        [InlineData(1)]
        [InlineData(2)]
        [InlineData(3)]
        [InlineData(4)]
        [InlineData(5)]
        public void TestAddingToCollections(int repetition)
        {
            integerSet.Add(1);
            integerList.Add(repetition);

            Assert.Equal(1, integerSet.Count);
            Assert.Equal(repetition, integerList.Count);
        }
    }
}