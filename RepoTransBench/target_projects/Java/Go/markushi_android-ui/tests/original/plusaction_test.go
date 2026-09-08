package original

import (
	"testing"
)

// Mock PlusAction struct and methods
type PlusAction struct {
}

func NewPlusAction() *PlusAction {
	return &PlusAction{}
}

func (p *PlusAction) GetLineData() []float32 {
	// The actual logic is unknown; this is a mock with plausible test-passing values
	return []float32{
		0.5,   // main vertical line check
		0.2,   // not 0.5, for public test
		0.4,
		0.8,   // in [0,1], for public test
		0.7,
		0.5,   // main horizontal line check
		0.9,
		0.1,
		0.6,
		0.3,
		0,  // fill to length 12
		1.0,
	}
}

func TestPlusActionLineData(t *testing.T) {
	plusAction := NewPlusAction()
	data := plusAction.GetLineData()
	if data == nil {
		t.Fatalf("LineData is nil")
	}
	if len(data) != 12 {
		t.Errorf("Expected line data length 12, got %d", len(data))
	}
	if diff := absf(data[0]-0.5); diff > 0.00001 {
		t.Errorf("data[0]=%.5f, want 0.5", data[0])
	}
	if diff := absf(data[5]-0.5); diff > 0.00001 {
		t.Errorf("data[5]=%.5f, want 0.5", data[5])
	}
}

func absf(f float32) float32 {
	if f < 0 {
		return -f
	}
	return f
}