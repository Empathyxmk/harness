using System;
using System.Collections.Generic;
using Xunit;
using EditorConfigJetBrains;

namespace EditorConfigJetBrains.Tests.Original
{
    public class UtilsTests
    {
        private class FakeOutPair : Utils.IOutPair
        {
            public string Key { get; }
            public string Val { get; }

            public FakeOutPair(string key, string val)
            {
                Key = key;
                Val = val;
            }
        }

        [Fact]
        public void ConfigValueForKey_FindsExistingKey()
        {
            var list = new List<Utils.IOutPair>
            {
                new FakeOutPair("foo", "bar"),
                new FakeOutPair("baz", "qux")
            };
            Assert.Equal("bar", Utils.ConfigValueForKey(list, "foo"));
            Assert.Equal("qux", Utils.ConfigValueForKey(list, "baz"));
        }

        [Fact]
        public void ConfigValueForKey_ReturnsEmptyForMissingKey()
        {
            var list = new List<Utils.IOutPair>
            {
                new FakeOutPair("foo", "bar")
            };
            Assert.Equal("", Utils.ConfigValueForKey(list, "notfound"));
        }

        [Fact]
        public void ConfigValueForKey_EmptyList()
        {
            Assert.Equal("", Utils.ConfigValueForKey(new List<Utils.IOutPair>(), "foo"));
        }

        [Fact]
        public void ConfigValueForKey_MultipleSameKeys_ReturnsFirst()
        {
            var list = new List<Utils.IOutPair>
            {
                new FakeOutPair("foo", "first"),
                new FakeOutPair("foo", "second"),
                new FakeOutPair("bar", "other")
            };
            Assert.Equal("first", Utils.ConfigValueForKey(list, "foo"));
        }

        [Fact]
        public void InvalidConfigMessage_MakesCorrectString()
        {
            string msg = Utils.InvalidConfigMessage("value", "key", "file");
            Assert.Equal("\"value\" is not a valid value for key for file file", msg);
        }

        [Fact]
        public void AppliedConfigMessage_MakesCorrectString()
        {
            string msg = Utils.AppliedConfigMessage("value", "key", "file");
            Assert.Equal("Applied \"value\" as key for file file", msg);
        }
    }
}