using Xunit;
using zfkun_ja_netfilter_mymap_plugin;
using zfkun_ja_netfilter_mymap_plugin.Models;
using System.Collections.Generic;

namespace zfkun_ja_netfilter_mymap_plugin.Tests.Original
{
    public class MapTransformerTests
    {
        [Fact]
        public void TestContainsRuleEqualMatch()
        {
            var rule = new FilterRule(RuleType.EQUAL, "test");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.True(transformer.ContainsRule("test"));
        }

        [Fact]
        public void TestContainsRuleEqualNoMatch()
        {
            var rule = new FilterRule(RuleType.EQUAL, "hello");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule("world"));
        }

        [Fact]
        public void TestContainsRuleContainsMatch()
        {
            var rule = new FilterRule(RuleType.CONTAINS, "abc");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.True(transformer.ContainsRule("123abc456"));
        }

        [Fact]
        public void TestContainsRuleNullInput()
        {
            var rule = new FilterRule(RuleType.EQUAL, "abc");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule(null));
        }

        [Fact]
        public void TestContainsRuleNullRuleType()
        {
            var rule = new FilterRule(null, "abc");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule("abc"));
        }

        [Fact]
        public void TestContainsRuleNullRule()
        {
            var rule = new FilterRule(RuleType.EQUAL, null);
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule("test"));
        }

        [Fact]
        public void TestContainsRuleMultipleRules()
        {
            var r1 = new FilterRule(RuleType.CONTAINS, "foo");
            var r2 = new FilterRule(RuleType.EQUAL, "bar");
            var transformer = new MapTransformer(new List<FilterRule> { r1, r2 });
            Assert.True(transformer.ContainsRule("foobar"));
            Assert.True(transformer.ContainsRule("bar"));
            Assert.False(transformer.ContainsRule("baz"));
        }

        [Fact]
        public void TestGetRules()
        {
            var rule = new FilterRule(RuleType.EQUAL, "abc");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.Equal(1, transformer.GetRules().Count);
        }
    }
}