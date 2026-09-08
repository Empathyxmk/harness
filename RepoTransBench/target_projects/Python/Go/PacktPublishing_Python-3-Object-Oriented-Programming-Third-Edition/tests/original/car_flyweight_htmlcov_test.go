package original

import (
	"bytes"
	"os"
	"testing"
	"github.com/packt-oop3/goport/internal/chapter11"
)

func TestCarModelSingletonBehaviorHTMLCov(t *testing.T) {
	m1 := chapter11.NewCarModel("Sedan", map[string]bool{"air": true})
	m2 := chapter11.NewCarModel("Sedan", map[string]bool{"air": false})
	if m1 != m2 {
		t.Error("Expected singleton: m1 should be the same as m2")
	}
	if m1.ModelName != "Sedan" {
		t.Error("Expected model name 'Sedan'")
	}
	// Should have air as True, as set in first instance
	if !m1.Air {
		t.Error("Expected air to be true after first instance")
	}
	if m1.AlloyWheels {
		t.Error("Expected AlloyWheels to be false by default")
	}
	m3 := chapter11.NewCarModel("Coupé", map[string]bool{"air": false, "tilt": true})
	if m3 == m1 {
		t.Error("m3 should not be the same singleton instance as m1")
	}
	if !m3.Tilt {
		t.Error("Expected tilt true for m3")
	}
	if m3.Air {
		t.Error("Expected air false for m3")
	}
}

func TestCarModelCheckSerialOutputHTMLCov(t *testing.T) {
	// Overwrite os.Stdout for capture
	r, w, _ := os.Pipe()
	stdout := os.Stdout
	os.Stdout = w
	defer func() { os.Stdout = stdout }()

	m := chapter11.NewCarModel("X", map[string]bool{"power_locks": true})
	m.CheckSerial("XYZ-123")
	_ = w.Close()
	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	out := buf.String()
	if !(contains(out, "XYZ-123") && contains(out, "X")) {
		t.Errorf("Output did not contain XYZ-123 and X, got: %v", out)
	}
}

func TestCarCheckSerialDelegatesHTMLCov(t *testing.T) {
	r, w, _ := os.Pipe()
	stdout := os.Stdout
	os.Stdout = w
	defer func() { os.Stdout = stdout }()

	m := chapter11.NewCarModel("TestModel", nil)
	c := chapter11.NewCar(m, "Red", 555)
	c.CheckSerial()
	_ = w.Close()
	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	out := buf.String()
	if !contains(out, "555") {
		t.Errorf("Output did not contain 555, got: %v", out)
	}
}

func TestCarAttributesHTMLCov(t *testing.T) {
	m := chapter11.NewCarModel("Z", nil)
	c := chapter11.NewCar(m, "Blue", 999)
	if c.Model != m {
		t.Error("Model not set correctly")
	}
	if c.Color != "Blue" {
		t.Error("Color not set")
	}
	if c.Serial != 999 {
		t.Error("Serial not set")
	}
}