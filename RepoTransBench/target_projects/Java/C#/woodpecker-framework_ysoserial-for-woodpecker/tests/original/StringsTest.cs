using System.Collections.Generic;
using Xunit;

namespace WoodpeckerYsoserial.Tests
{
    public class StringsTest
    {
        [Fact]
        public void TestJoinSimple()
        {
            var items = new List<string>() { "a", "b", "c" };
            Assert.Equal("a,b,c", Strings.Join(items, ",", "", ""));
        }

        [Fact]
        public void TestJoinWithPrefixSuffix()
        {
            var items = new List<string>() { "a", "b" };
            Assert.Equal("@a@|@b@", Strings.Join(items, "|", "@", "@"));
        }

        [Fact]
        public void TestRepeat()
        {
            Assert.Equal("aaa", Strings.Repeat("a", 3));
            Assert.Equal("", Strings.Repeat("a", 0));
        }

        [Fact]
        public void TestFormatTable()
        {
            var rows = new List<string[]>
            {
                new string[] { "ColA", "ColB" },
                new string[] { "1", "22" },
                new string[] { "333", "4" }
            };
            var formatted = Strings.FormatTable(rows);
            Assert.Equal(3, formatted.Count);
            Assert.StartsWith("ColA", formatted[0]);
        }

        [Fact]
        public void TestFormatTableMismatchedThrows()
        {
            var rows = new List<string[]>
            {
                new string[] { "ColA", "ColB" },
                new string[] { "1" }
            };
            Assert.Throws<System.InvalidOperationException>(() => Strings.FormatTable(rows));
        }

        [Fact]
        public void TestToStringComparator()
        {
            var cmp = new Strings.ToStringComparator();
            Assert.True(cmp.Compare("aaa", "bbb") < 0);
            Assert.Equal(0, cmp.Compare("test", "test"));
            Assert.True(cmp.Compare("zzz", "aaa") > 0);
        }
    }
}