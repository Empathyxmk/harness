package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"zfkun_ja_netfilter_mymap_plugin/tests"
)

func TestAllowWithNullRulesPublic(t *testing.T) {
	putFilter := tests.NewPutFilter(nil)
	assert.True(t, putFilter.ShouldAllow("someKey"))
}

func TestAllowWithEmptyRulesPublic(t *testing.T) {
	putFilter := tests.NewPutFilter([]*tests.FilterRule{})
	assert.True(t, putFilter.ShouldAllow("anotherKey"))
}

func TestAllowWithNullKeyPublic(t *testing.T) {
	v := "foo"
	rule := tests.NewFilterRule(&tests.CONTAINS, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.True(t, putFilter.ShouldAllow(""))
}

func TestBlockEqualRulePublic(t *testing.T) {
	v := "deny"
	rule := tests.NewFilterRule(&tests.EQUAL, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.False(t, putFilter.ShouldAllow("deny"))
	assert.True(t, putFilter.ShouldAllow("DENY"))
}

func TestBlockContainsRulePublic(t *testing.T) {
	v := "testz"
	rule := tests.NewFilterRule(&tests.CONTAINS, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.False(t, putFilter.ShouldAllow("exec_testz_helper"))
	assert.True(t, putFilter.ShouldAllow("basic_helper"))
}

func TestAllowWithUnknownTypePublic(t *testing.T) {
	v := "nothing"
	rule := tests.NewFilterRule(nil, &v)
	putFilter := tests.NewPutFilter([]*tests.FilterRule{rule})
	assert.True(t, putFilter.ShouldAllow("nothing"))
}

func TestAllowWithNullRulePublic(t *testing.T) {
	putFilter := tests.NewPutFilter([]*tests.FilterRule{
		nil,
		tests.NewFilterRule(&tests.EQUAL, nil),
	})
	assert.True(t, putFilter.ShouldAllow("foobar"))
}

func TestMultipleRulesPublic(t *testing.T) {
	r1 := tests.NewFilterRule(&tests.EQUAL, strPtr("firsty"))
	r2 := tests.NewFilterRule(&tests.CONTAINS, strPtr("r3d"))
	putFilter := tests.NewPutFilter([]*tests.FilterRule{r1, r2})
	assert.False(t, putFilter.ShouldAllow("firsty"))
	assert.False(t, putFilter.ShouldAllow("meshr3dmesh"))
	assert.True(t, putFilter.ShouldAllow("totallyDifferent"))
}

func strPtr(s string) *string { return &s }