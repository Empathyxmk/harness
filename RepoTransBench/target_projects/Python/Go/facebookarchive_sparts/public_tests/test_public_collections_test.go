package public_tests

import "testing"

// Dummy test to ensure file runs and collects.
func TestPublicCollectionsBasic(t *testing.T) {
	if 5+7 != 12 {
		t.Error("5+7 should be 12")
	}
	if "sparts"[:3] != "spa" {
		t.Error(`"sparts"[:3] != "spa"`)
	}
}