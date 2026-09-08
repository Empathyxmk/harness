package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"zfkun_ja_netfilter_mymap_plugin/tests"
)

func TestContainsRuleEqualMatchPublic(t *testing.T) {
	v := "publicValue"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.True(t, transformer.ContainsRule("publicValue"))
}

func TestContainsRuleEqualNoMatchPublic(t *testing.T) {
	v := "apple"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule("orange"))
}

func TestContainsRuleContainsMatchPublic(t *testing.T) {
	v := "uvw"
	rule := tests.NewFilterRule(&tests.CONTAINS, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.True(t, transformer.ContainsRule("123uvwx456"))
}

func TestContainsRuleNullInputPublic(t *testing.T) {
	v := "xyz"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule(""))
}

func TestContainsRuleNullRuleTypePublic(t *testing.T) {
	v := "banana"
	rule := tests.NewFilterRule(nil, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule("banana"))
}

func TestContainsRuleNullRulePublic(t *testing.T) {
	rule := tests.NewFilterRule(&tests.EQUAL, nil)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule("AlphaTest"))
}

func TestContainsRuleMultipleRulesPublic(t *testing.T) {
	v1 := "abc"
	v2 := "xyz123"
	r1 := tests.NewFilterRule(&tests.CONTAINS, &v1)
	r2 := tests.NewFilterRule(&tests.EQUAL, &v2)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{r1, r2})
	assert.True(t, transformer.ContainsRule("loremabcipso"))
	assert.True(t, transformer.ContainsRule("xyz123"))
	assert.False(t, transformer.ContainsRule("hello world"))
}

func TestGetRulesPublic(t *testing.T) {
	v := "public"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.Equal(t, 1, len(transformer.GetRules()))
}