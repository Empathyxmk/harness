using System;
using System.Collections.Generic;
using Xunit;
using EditorConfigJetBrains;

namespace EditorConfigJetBrains.PublicTests
{
    public class UtilsPublicTests
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
        public void ConfigValueForKey_FindsDifferentExistingKey()
        {
            var list = new List<Utils.IOutPair>
            {
                new FakeOutPair("alpha", "beta"),
                new FakeOutPair("gamma", "delta")
            };
            Assert.Equal("beta", Utils.ConfigValueForKey(list, "alpha"));
            Assert.Equal("delta", Utils.ConfigValueForKey(list, "gamma"));
        }

        [Fact]
        public void ConfigValueForKey_ReturnsEmptyForAnotherMissingKey()
        {
            var list = new List<Utils.IOutPair>
            {
                new FakeOutPair("one", "two")
            };
            Assert.Equal("", Utils.ConfigValueForKey(list, "absent"));
        }

        [Fact]
        public void ConfigValueForKey_EmptyList_StillReturnsEmpty()
        {
            Assert.Equal("", Utils.ConfigValueForKey(new List<Utils.IOutPair>(), "doesnotexist"));
        }

        [Fact]
        public void ConfigValueForKey_MultipleSameKeys_ReturnsFirstPublic()
        {
            var list = new List<Utils.IOutPair>
            {
                new FakeOutPair("dup", "uno"),
                new FakeOutPair("dup", "dos"),
                new FakeOutPair("other", "tres")
            };
            Assert.Equal("uno", Utils.ConfigValueForKey(list, "dup"));
        }

        [Fact]
        public void InvalidConfigMessage_MakesCorrectStringPublic()
        {
            string msg = Utils.InvalidConfigMessage("42", "answer", "deepfile");
            Assert.Equal("\"42\" is not a valid value for key for file deepfile", msg);
        }

        [Fact]
        public void AppliedConfigMessage_MakesCorrectStringPublic()
        {
            string msg = Utils.AppliedConfigMessage("enabled", "feature", "file.txt");
            Assert.Equal("Applied \"enabled\" as key for file file.txt", msg);
        }
    }
}