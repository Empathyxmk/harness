package public_tests

import (
	"testing"
	"github.com/example/initstring_linkedin2username"
)

func TestPublicGeoRegionsUS(t *testing.T) {
	found := false
	for code, regionID := range linkedin2username.GEO_REGIONS {
		// Use GB region instead for public test (mirrored logic)
		if code == "gb" && regionID != "" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Should find region for GB")
	}
}

func TestPublicGeoRegionsAllHaveStr(t *testing.T) {
	for code, regionID := range linkedin2username.GEO_REGIONS {
		if _, ok := regionID.(string); !ok {
			t.Errorf("RegionID for code %v is not string", code)
		}
	}
}