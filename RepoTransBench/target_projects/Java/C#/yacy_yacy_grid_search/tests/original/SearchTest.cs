using System;
using Xunit;
using YacyGridSearch;

namespace YacyGridSearch.Tests.Original
{
    public class SearchTest
    {
        [Fact]
        public void TestQueryNormal()
        {
            var s = new Search();
            Assert.Equal("Search results for: hello", s.Query("hello"));
        }

        [Fact]
        public void TestQueryEmpty()
        {
            var s = new Search();
            Assert.Equal("No query provided", s.Query(""));
            Assert.Equal("No query provided", s.Query(null));
            Assert.Equal("No query provided", s.Query("  "));
        }

        [Fact]
        public void TestQueryError()
        {
            var s = new Search();
            var ex = Assert.Throws<ArgumentException>(() => s.Query("error"));
            Assert.Equal("Invalid query", ex.Message);
        }

        [Fact]
        public void TestIsServiceActive()
        {
            var s = new Search();
            Assert.True(s.IsServiceActive());
        }
    }
}