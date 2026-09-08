package public_tests

import (
	"testing"
	"markushi_android_ui/tests/original"
)

func TestDrawerActionLineDataPublic(t *testing.T) {
	drawerAction := original.NewDrawerAction()
	data := drawerAction.GetLineData()
	if data == nil {
		t.Fatalf("LineData is nil")
	}
	if len(data) != 12 {
		t.Errorf("Expected line data length 12, got %d", len(data))
	}
	// check a value not checked in the original (index 7)
	if data[7] < 0.0 || data[7] > 1.0 {
		t.Errorf("data[7]=%.5f not in [0,1]", data[7])
	}
	// ensure at least one line does NOT have 0.5f value at a new index
	if absf(data[2]-0.5) < 0.00001 {
		t.Errorf("data[2]=%.5f, should NOT be 0.5", data[2])
	}
}

func absf(f float32) float32 {
	if f < 0 {
		return -f
	}
	return f
}