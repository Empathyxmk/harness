package original

import (
	"strings"
	"testing"
	"yahoo-historical-go/yah"
)

// This is for htmlcov/d_a44f0ac069e85531_test_constants_py.html coverage.

func TestConstantsHtmlcovDImport2(t *testing.T) {
	_ = yah.Constants{}
}
func TestConstantsHtmlcovDURLDictOrList2(t *testing.T) {
	c := yah.Constants{}
	found := false
	for _, k := range c.Keys() {
		if strings.Contains(k, "URL") {
			val := c.GetByKey(k)
			switch val.(type) {
			case map[string]interface{}, string, []interface{}:
			default:
				t.Errorf("%s is not dict, str, or list: %T", k, val)
			}
			found = true
		}
	}
	if !found {
		t.Error("No URL-like constants found")
	}
}
func TestConstantsHtmlcovDConstantValues2(t *testing.T) {
	c := yah.Constants{}
	if c.Has("URLS") {
		if _, ok := c.GetByKey("URLS").(map[string]interface{}); !ok {
			t.Error("URLS is not a map")
		}
	}
	if c.Has("ONE_DAY_INTERVAL") {
		if _, ok := c.GetByKey("ONE_DAY_INTERVAL").(string); !ok {
			t.Error("ONE_DAY_INTERVAL is not a string")
		}
	}
}
func TestConstantsHtmlcovDModuleStr2(t *testing.T) {
	c := yah.Constants{}
	if s := c.String(); s == "" {
		t.Error("Constants String() is empty")
	}
	if r := c.Repr(); r == "" {
		t.Error("Constants Repr() is empty")
	}
}