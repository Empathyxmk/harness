using System.Collections.Generic;
using Xunit;

namespace DavidMoten.Geo.Tests
{
    public class CoverageTest
    {
        [Fact]
        public void TestGetHashesReturnsSameSet()
        {
            var h = new HashSet<string> { "abc123" };
            var c = new Coverage(h, 2.5);
            Assert.Equal(h, c.Hashes);
        }

        [Fact]
        public void TestGetRatio()
        {
            var h = new HashSet<string> { "abc123" };
            var c = new Coverage(h, 2.7);
            Assert.Equal(2.7, c.Ratio, 5);
        }

        [Fact]
        public void TestGetHashLengthWithEmptySet()
        {
            var c = new Coverage(new HashSet<string>(), 1.0);
            Assert.Equal(0, c.HashLength);
        }

        [Fact]
        public void TestGetHashLengthWithNonEmptySet()
        {
            var set = new SortedSet<string> { "aaaa" };
            var c = new Coverage(set, 1.1);
            Assert.Equal(4, c.HashLength);
        }

        [Fact]
        public void TestToString()
        {
            var hashes = new SortedSet<string> { "hash1" };
            var c = new Coverage(hashes, 3.14);
            string s = c.ToString();
            Assert.Contains("hashes", s);
            Assert.Contains("ratio", s);
        }
    }
}