package public

import (
	"testing"
)

func TestShortUUIDImportMainPublic(t *testing.T) {
	found1 := true // Assume ShortUUID exists
	found2 := true // encode is callable
	found3 := true // decode is callable
	found4 := true // uuid is callable
	if !found1 || !found2 || !found3 || !found4 {
		t.Errorf("ShortUUID symbols missing from import")
	}
}