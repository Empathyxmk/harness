using Xunit;
using zfkun_ja_netfilter_mymap_plugin;
using zfkun_ja_netfilter_mymap_plugin.Models;
using System.Collections.Generic;

namespace zfkun_ja_netfilter_mymap_plugin.PublicTests
{
    public class PutFilterPublicTests
    {
        [Fact]
        public void TestAllowWithNullRules_Public()
        {
            var putFilter = new PutFilter(null);
            Assert.True(putFilter.ShouldAllow("someKey"));
        }

        [Fact]
        public void TestAllowWithEmptyRules_Public()
        {
            var putFilter = new PutFilter(new List<FilterRule>());
            Assert.True(putFilter.ShouldAllow("anotherKey"));
        }

        [Fact]
        public void TestAllowWithNullKey_Public()
        {
            var rule = new FilterRule(RuleType.CONTAINS, "foo");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.True(putFilter.ShouldAllow(null));
        }

        [Fact]
        public void TestBlockEqualRule_Public()
        {
            var rule = new FilterRule(RuleType.EQUAL, "deny");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.False(putFilter.ShouldAllow("deny"));
            Assert.True(putFilter.ShouldAllow("DENY")); // still case-sensitive
        }

        [Fact]
        public void TestBlockContainsRule_Public()
        {
            var rule = new FilterRule(RuleType.CONTAINS, "testz");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.False(putFilter.ShouldAllow("exec_testz_helper"));
            Assert.True(putFilter.ShouldAllow("basic_helper"));
        }

        [Fact]
        public void TestAllowWithUnknownType_Public()
        {
            var rule = new FilterRule(null, "nothing");
            var putFilter = new PutFilter(new List<FilterRule> { rule });
            Assert.True(putFilter.ShouldAllow("nothing"));
        }

        [Fact]
        public void TestAllowWithNullRule_Public()
        {
            var putFilter = new PutFilter(new List<FilterRule>
            {
                null,
                new FilterRule(RuleType.EQUAL, null)
            });
            Assert.True(putFilter.ShouldAllow("foobar"));
        }

        [Fact]
        public void TestMultipleRules_Public()
        {
            var r1 = new FilterRule(RuleType.EQUAL, "firsty");
            var r2 = new FilterRule(RuleType.CONTAINS, "r3d");
            var putFilter = new PutFilter(new List<FilterRule> { r1, r2 });
            Assert.False(putFilter.ShouldAllow("firsty"));
            Assert.False(putFilter.ShouldAllow("meshr3dmesh"));
            Assert.True(putFilter.ShouldAllow("totallyDifferent"));
        }
    }
}