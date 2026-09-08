package original

import (
	"strings"
	"testing"
	"yahoo-historical-go/yah"
)

func TestConstantsImport(t *testing.T) {
	_ = yah.Constants{}
}

func TestURLDictOrList(t *testing.T) {
	c := yah.Constants{}
	anyURLkey := false
	for _, name := range c.Keys() {
		if strings.Contains(name, "URL") {
			val := c.GetByKey(name)
			switch val.(type) {
			case map[string]interface{}, string, []interface{}:
				anyURLkey = true
			default:
				t.Errorf("%s is not dict, str, or list: %T", name, val)
			}
		}
	}
	if !anyURLkey {
		t.Error("No URL-like constants found")
	}
}

func TestConstantValues(t *testing.T) {
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

func TestConstantModuleStr(t *testing.T) {
	c := yah.Constants{}
	if c.String() == "" {
		t.Error("Constants String() is empty")
	}
	if c.Repr() == "" {
		t.Error("Constants Repr() is empty")
	}
}

func TestAllConstantSymbolsAccounted(t *testing.T) {
	c := yah.Constants{}
	for _, attr := range c.UpperKeys() {
		val := c.GetByKey(attr)
		switch val.(type) {
		case string, map[string]interface{}, []interface{}, int, float64:
			// OK
		default:
			t.Errorf("Unexpected type for key %s: %T", attr, val)
		}
	}
}

func TestModuleDirSubset(t *testing.T) {
	c := yah.Constants{}
	found := false
	for _, s := range c.Dir() {
		if s == "__name__" {
			found = true
		}
	}
	if !found {
		t.Error("__name__ not in Constants.Dir()")
	}
}