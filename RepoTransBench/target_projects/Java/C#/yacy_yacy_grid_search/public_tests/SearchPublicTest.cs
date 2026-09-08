using System;
using Xunit;
using YacyGridSearch;

namespace YacyGridSearch.Tests.Public
{
    public class SearchPublicTest
    {
        [Fact]
        public void TestQueryNormal()
        {
            var s = new Search();
            Assert.Equal("Search results for: world", s.Query("world"));
            Assert.Equal("Search results for: 123", s.Query("123"));
            Assert.Equal("Search results for: test_case", s.Query("test_case"));
        }

        [Fact]
        public void TestQueryEmptyVariants()
        {
            var s = new Search();
            Assert.Equal("No query provided", s.Query("   "));
            Assert.Equal("No query provided", s.Query(null));
            Assert.Equal("No query provided", s.Query("\t"));
        }

        [Fact]
        public void TestQueryErrorDifferentCase()
        {
            var s = new Search();
            var ex = Assert.Throws<ArgumentException>(() => s.Query("ERROR"));
            Assert.Equal("Invalid query", ex.Message);
            var ex2 = Assert.Throws<ArgumentException>(() => s.Query("Error"));
            Assert.Equal("Invalid query", ex2.Message);
        }

        [Fact]
        public void TestIsServiceActiveStillTrue()
        {
            var s = new Search();
            Assert.True(s.IsServiceActive());
        }
    }
}