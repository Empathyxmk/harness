package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"zfkun_ja_netfilter_mymap_plugin/tests"
)

func TestAllowWithNullRules(t *testing.T) {
	putFilter := tests.NewPutFilter(nil)
	assert.True(t, putFilter.ShouldAllow("key"))
}

func TestAllowWithEmptyRules(t *testing.T) {
	putFilter := tests.NewPutFilter([]*tests.FilterRule{})
	assert.True(t, putFilter.ShouldAllow("key"))
}

func TestAllowWithNullKey(t *testing.T) {
	v := "bar"
	rule := tests.NewFilterRule(&tests.CONTAINS, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.True(t, putFilter.ShouldAllow(""))
}

func TestBlockEqualRule(t *testing.T) {
	v := "block"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.False(t, putFilter.ShouldAllow("block"))
	assert.True(t, putFilter.ShouldAllow("BLOCK"))
}

func TestBlockContainsRule(t *testing.T) {
	v := "xyz"
	rule := tests.NewFilterRule(&tests.CONTAINS, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.False(t, putFilter.ShouldAllow("helloxyzworld"))
	assert.True(t, putFilter.ShouldAllow("helloworld"))
}

func TestAllowWithUnknownType(t *testing.T) {
	v := "block"
	rule := tests.NewFilterRule(nil, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.True(t, putFilter.ShouldAllow("block"))
}

func TestAllowWithNullRule(t *testing.T) {
	putFilter := tests.NewPutFilter([]*tests.FilterRule{
		nil,
		tests.NewFilterRule(&tests.EQUAL, nil),
	})
	assert.True(t, putFilter.ShouldAllow("something"))
}

func TestMultipleRules(t *testing.T) {
	r1 := tests.NewFilterRule(&tests.EQUAL, strPtr("a"))
	r2 := tests.NewFilterRule(&tests.CONTAINS, strPtr("bc"))
	putFilter := tests.NewPutFilter([]*tests.FilterRule{r1, r2})
	assert.False(t, putFilter.ShouldAllow("a"))
	assert.False(t, putFilter.ShouldAllow("bcd"))
	assert.True(t, putFilter.ShouldAllow("xyz"))
}

func strPtr(s string) *string { return &s }