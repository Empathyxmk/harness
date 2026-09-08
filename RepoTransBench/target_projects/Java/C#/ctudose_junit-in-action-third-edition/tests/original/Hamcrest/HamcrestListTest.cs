using Xunit;
using System.Collections.Generic;
using FluentAssertions;

namespace OriginalTests.Hamcrest
{
    public class HamcrestListTest
    {
        private List<string> _customersNames;

        public HamcrestListTest()
        {
            _customersNames = new List<string> { "John", "Michael", "Edwin" };
        }

        [Fact]
        public void TestListWithoutHamcrest()
        {
            bool contains = _customersNames.Contains("John") ||
                            _customersNames.Contains("Michael") ||
                            _customersNames.Contains("Edwin");
            Assert.True(contains);
        }

        [Fact]
        public void TestListWithHamcrest()
        {
            _customersNames.Should().Contain("John")
                .And.Contain("Michael")
                .And.Contain("Edwin");
        }
    }
}