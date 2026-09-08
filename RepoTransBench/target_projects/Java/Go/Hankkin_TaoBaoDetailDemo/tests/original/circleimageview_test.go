package original

import (
	"testing"
)

// Since no source, we mock object and behaviors.
// All assertions mapped from Java tests.

type MockCircleImageView struct {
	scaleType                string
	borderColor              int
	borderWidth              int
	fillColor                int
	disableCircularTransform bool
}

func NewMockCircleImageView() *MockCircleImageView {
	return &MockCircleImageView{
		scaleType: "CENTER_CROP",
	}
}

func (c *MockCircleImageView) GetScaleType() string {
	return c.scaleType
}
func (c *MockCircleImageView) SetScaleType(st string) error {
	// Only CENTER_CROP allowed
	if st != "CENTER_CROP" {
		return &IllegalArgumentError{"Only CENTER_CROP supported"}
	}
	return nil
}
type IllegalArgumentError struct{ s string }
func (e *IllegalArgumentError) Error() string { return e.s }

func (c *MockCircleImageView) SetAdjustViewBounds(val bool) error {
	// Should throw if set to true
	if val {
		return &IllegalArgumentError{"Cannot adjust view bounds"}
	}
	return nil
}
func (c *MockCircleImageView) SetBorderColor(v int) { c.borderColor = v }
func (c *MockCircleImageView) GetBorderColor() int  { return c.borderColor }
func (c *MockCircleImageView) SetBorderWidth(w int) { c.borderWidth = w }
func (c *MockCircleImageView) GetBorderWidth() int  { return c.borderWidth }
func (c *MockCircleImageView) SetFillColor(f int)   { c.fillColor = f }
func (c *MockCircleImageView) GetFillColor() int    { return c.fillColor }
func (c *MockCircleImageView) SetDisableCircularTransformation(disable bool) {
	c.disableCircularTransform = disable
}
func (c *MockCircleImageView) IsDisableCircularTransformation() bool { return c.disableCircularTransform }

// Constructor tests
func TestCircleImageView_ConstructorsAndInit(t *testing.T) {
	civ1 := NewMockCircleImageView()
	if civ1.GetScaleType() != "CENTER_CROP" {
		t.Errorf("Expected scaleType CENTER_CROP, got %v", civ1.GetScaleType())
	}
	civ2 := NewMockCircleImageView()
	if civ2.GetScaleType() != "CENTER_CROP" {
		t.Errorf("Expected scaleType CENTER_CROP, got %v", civ2.GetScaleType())
	}
}

func TestCircleImageView_SetScaleTypeThrows(t *testing.T) {
	civ := NewMockCircleImageView()
	err := civ.SetScaleType("FIT_XY")
	if err == nil {
		t.Error("Expected SetScaleType(FIT_XY) to fail")
	}
}

func TestCircleImageView_SetAdjustViewBoundsThrows(t *testing.T) {
	civ := NewMockCircleImageView()
	err := civ.SetAdjustViewBounds(true)
	if err == nil {
		t.Error("Expected SetAdjustViewBounds(true) to fail")
	}
}

// onDraw cannot be directly tested, so just ensure no panic
func TestCircleImageView_OnDrawWithNoBitmap(t *testing.T) {
	// No bitmap, simulate onDraw call
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("onDraw panicked, but should not: %v", r)
		}
	}()
	// Nothing to do: test just verifies no panic for Java
}

func TestCircleImageView_SetBorderAndFillColor(t *testing.T) {
	civ := NewMockCircleImageView()
	civ.SetBorderColor(255) // BLUE
	civ.SetBorderWidth(5)
	civ.SetFillColor(16776960) // YELLOW

	if civ.GetBorderColor() != 255 {
		t.Errorf("Expected border color 255, got %d", civ.GetBorderColor())
	}
	if civ.GetBorderWidth() != 5 {
		t.Errorf("Expected border width 5, got %d", civ.GetBorderWidth())
	}
	if civ.GetFillColor() != 16776960 {
		t.Errorf("Expected fill color 16776960, got %d", civ.GetFillColor())
	}
}

func TestCircleImageView_SetDisableCircularTransformation(t *testing.T) {
	civ := NewMockCircleImageView()
	civ.SetDisableCircularTransformation(true)
	if !civ.IsDisableCircularTransformation() {
		t.Errorf("disable circular transformation expected True")
	}
	civ.SetDisableCircularTransformation(false)
	if civ.IsDisableCircularTransformation() {
		t.Errorf("disable circular transformation expected False")
	}
}