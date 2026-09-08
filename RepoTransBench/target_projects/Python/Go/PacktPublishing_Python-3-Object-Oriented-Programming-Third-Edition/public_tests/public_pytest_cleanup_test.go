package public_tests

import (
	"testing"
)

type DangerZone struct {
	Code    string
	IsClean bool
}

func (dz *DangerZone) Clean() {
	dz.IsClean = true
}

func dangerZonePublic() *DangerZone {
	return &DangerZone{Code: "DZ-909", IsClean: false}
}

func TestCleanupActionPublic(t *testing.T) {
	dz := dangerZonePublic()
	if dz.IsClean {
		t.Errorf("Expected dz not clean at start")
	}
}

func TestCleanupFinalizePublic(t *testing.T) {
	dz := dangerZonePublic()
	dz.Clean()
	if !dz.IsClean {
		t.Errorf("Cleanup did not set IsClean true")
	}
}