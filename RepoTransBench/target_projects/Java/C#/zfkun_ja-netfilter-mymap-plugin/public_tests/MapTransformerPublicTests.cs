using Xunit;
using zfkun_ja_netfilter_mymap_plugin;
using zfkun_ja_netfilter_mymap_plugin.Models;
using System.Collections.Generic;

namespace zfkun_ja_netfilter_mymap_plugin.PublicTests
{
    public class MapTransformerPublicTests
    {
        [Fact]
        public void TestContainsRuleEqualMatch_Public()
        {
            var rule = new FilterRule(RuleType.EQUAL, "publicValue");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.True(transformer.ContainsRule("publicValue"));
        }

        [Fact]
        public void TestContainsRuleEqualNoMatch_Public()
        {
            var rule = new FilterRule(RuleType.EQUAL, "apple");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule("orange"));
        }

        [Fact]
        public void TestContainsRuleContainsMatch_Public()
        {
            var rule = new FilterRule(RuleType.CONTAINS, "uvw");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.True(transformer.ContainsRule("123uvwx456"));
        }

        [Fact]
        public void TestContainsRuleNullInput_Public()
        {
            var rule = new FilterRule(RuleType.EQUAL, "xyz");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule(null));
        }

        [Fact]
        public void TestContainsRuleNullRuleType_Public()
        {
            var rule = new FilterRule(null, "banana");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule("banana"));
        }

        [Fact]
        public void TestContainsRuleNullRule_Public()
        {
            var rule = new FilterRule(RuleType.EQUAL, null);
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.False(transformer.ContainsRule("AlphaTest"));
        }

        [Fact]
        public void TestContainsRuleMultipleRules_Public()
        {
            var r1 = new FilterRule(RuleType.CONTAINS, "abc");
            var r2 = new FilterRule(RuleType.EQUAL, "xyz123");
            var transformer = new MapTransformer(new List<FilterRule> { r1, r2 });
            Assert.True(transformer.ContainsRule("loremabcipso"));
            Assert.True(transformer.ContainsRule("xyz123"));
            Assert.False(transformer.ContainsRule("hello world"));
        }

        [Fact]
        public void TestGetRules_Public()
        {
            var rule = new FilterRule(RuleType.EQUAL, "public");
            var transformer = new MapTransformer(new List<FilterRule> { rule });
            Assert.Equal(1, transformer.GetRules().Count);
        }
    }
}