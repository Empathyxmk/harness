package public_tests

import (
	"testing"
	"markushi_android_ui/tests/original"
)

func TestPlusActionLineDataPublic(t *testing.T) {
	plusAction := original.NewPlusAction()
	data := plusAction.GetLineData()
	if data == nil {
		t.Fatalf("LineData is nil")
	}
	if len(data) != 12 {
		t.Errorf("Expected line data length 12, got %d", len(data))
	}
	if absf(data[1]-0.5) < 0.00001 {
		t.Errorf("data[1]=%.5f, should NOT be 0.5", data[1])
	}
	if data[3] < 0 || data[3] > 1 {
		t.Errorf("data[3]=%.5f, want in [0,1]", data[3])
	}
}

func absf(f float32) float32 {
	if f < 0 {
		return -f
	}
	return f
}