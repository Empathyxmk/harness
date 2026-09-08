using Xunit;
using zfkun_ja_netfilter_mymap_plugin;
using zfkun_ja_netfilter_mymap_plugin.Models;
using System.Collections.Generic;

namespace zfkun_ja_netfilter_mymap_plugin.Tests.Original
{
    public class PutFilterTests
    {
        [Fact]
        public void TestAllowWithNullRules()
        {
            var putFilter = new PutFilter(null);
            Assert.True(putFilter.ShouldAllow("key"));
        }

        [Fact]
        public void TestAllowWithEmptyRules()
        {
            var putFilter = new PutFilter(new List<FilterRule>());
            Assert.True(putFilter.ShouldAllow("key"));
        }

        [Fact]
        public void TestAllowWithNullKey()
        {
            var rule = new FilterRule(RuleType.CONTAINS, "bar");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.True(putFilter.ShouldAllow(null));
        }

        [Fact]
        public void TestBlockEqualRule()
        {
            var rule = new FilterRule(RuleType.EQUAL, "block");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.False(putFilter.ShouldAllow("block"));
            Assert.True(putFilter.ShouldAllow("BLOCK")); // case-sensitive
        }

        [Fact]
        public void TestBlockContainsRule()
        {
            var rule = new FilterRule(RuleType.CONTAINS, "xyz");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.False(putFilter.ShouldAllow("helloxyzworld"));
            Assert.True(putFilter.ShouldAllow("helloworld"));
        }

        [Fact]
        public void TestAllowWithUnknownType()
        {
            var rule = new FilterRule(null, "block");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.True(putFilter.ShouldAllow("block"));
        }

        [Fact]
        public void TestAllowWithNullRule()
        {
            var putFilter = new PutFilter(new List<FilterRule>
            {
                null,
                new FilterRule(RuleType.EQUAL, null)
            });
            Assert.True(putFilter.ShouldAllow("something"));
        }

        [Fact]
        public void TestMultipleRules()
        {
            var r1 = new FilterRule(RuleType.EQUAL, "a");
            var r2 = new FilterRule(RuleType.CONTAINS, "bc");
            var putFilter = new PutFilter(new List<FilterRule> { r1, r2 });
            Assert.False(putFilter.ShouldAllow("a"));
            Assert.False(putFilter.ShouldAllow("bcd"));
            Assert.True(putFilter.ShouldAllow("xyz"));
        }
    }
}