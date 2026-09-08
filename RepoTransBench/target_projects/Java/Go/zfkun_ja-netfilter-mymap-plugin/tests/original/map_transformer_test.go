package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"zfkun_ja_netfilter_mymap_plugin/tests"
)

func TestContainsRuleEqualMatch(t *testing.T) {
	v := "test"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.True(t, transformer.ContainsRule("test"))
}

func TestContainsRuleEqualNoMatch(t *testing.T) {
	v := "hello"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule("world"))
}

func TestContainsRuleContainsMatch(t *testing.T) {
	v := "abc"
	rule := tests.NewFilterRule(&tests.CONTAINS, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.True(t, transformer.ContainsRule("123abc456"))
}

func TestContainsRuleNullInput(t *testing.T) {
	v := "abc"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule(""))
}

func TestContainsRuleNullRuleType(t *testing.T) {
	v := "abc"
	rule := tests.NewFilterRule(nil, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule("abc"))
}

func TestContainsRuleNullRule(t *testing.T) {
	rule := tests.NewFilterRule(&tests.EQUAL, nil)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.False(t, transformer.ContainsRule("test"))
}

func TestContainsRuleMultipleRules(t *testing.T) {
	v1 := "foo"
	v2 := "bar"
	r1 := tests.NewFilterRule(&tests.CONTAINS, &v1)
	r2 := tests.NewFilterRule(&tests.EQUAL, &v2)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{r1, r2})
	assert.True(t, transformer.ContainsRule("foobar"))
	assert.True(t, transformer.ContainsRule("bar"))
	assert.False(t, transformer.ContainsRule("baz"))
}

func TestGetRules(t *testing.T) {
	v := "abc"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	transformer := tests.NewMapTransformer([]*tests.FilterRule{rule})
	assert.Equal(t, 1, len(transformer.GetRules()))
}