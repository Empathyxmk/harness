package original

import (
	"testing"
	"github.com/example/initstring_linkedin2username"
	"reflect"
)

func TestGeoRegionsUS(t *testing.T) {
	if val, ok := linkedin2username.GEO_REGIONS["us"]; !ok || val != "103644278" {
		t.Errorf(`Expected GEO_REGIONS["us"] == "103644278", got %v`, val)
	}
}

func TestGeoRegionsAllHaveStr(t *testing.T) {
	for code, val := range linkedin2username.GEO_REGIONS {
		if reflect.TypeOf(code).Kind() != reflect.String {
			t.Errorf("Geo code %v not a string", code)
		}
		if reflect.TypeOf(val).Kind() != reflect.String {
			t.Errorf("Geo value %v not a string", val)
		}
		for _, ch := range val {
			if ch < '0' || ch > '9' {
				t.Errorf("Geo region value %v is not all digits", val)
				break
			}
		}
	}
}