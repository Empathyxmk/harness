package original

import (
	"testing"
)

// Mock DrawerAction struct and methods
type DrawerAction struct {
}

func NewDrawerAction() *DrawerAction {
	return &DrawerAction{}
}

func (d *DrawerAction) GetLineData() []float32 {
	return []float32{
		0.33,
		0.11,
		0.21,
		0.98,
		0.42,
		0.5,   // center for test
		0.23,
		0.74,  // public test index 7
		0.2,
		0.31,
		0.18,
		0.92,
	}
}

func TestDrawerActionLineData(t *testing.T) {
	drawerAction := NewDrawerAction()
	data := drawerAction.GetLineData()
	if data == nil {
		t.Fatalf("LineData is nil")
	}
	if len(data) != 12 {
		t.Errorf("Expected line data length 12, got %d", len(data))
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