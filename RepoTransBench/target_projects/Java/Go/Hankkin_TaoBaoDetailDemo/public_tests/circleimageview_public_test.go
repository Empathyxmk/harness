package public_tests

import (
	"testing"
)

// Simulate CircleImageView
type CircleImageViewPublic struct {
	borderColor   int
	borderWidth   int
	fillColor     int
	borderOverlay bool
}

func NewCircleImageViewPublic() *CircleImageViewPublic {
	return &CircleImageViewPublic{}
}
func (c *CircleImageViewPublic) SetBorderColor(val int) { c.borderColor = val }
func (c *CircleImageViewPublic) GetBorderColor() int    { return c.borderColor }
func (c *CircleImageViewPublic) SetBorderWidth(w int)   { c.borderWidth = w }
func (c *CircleImageViewPublic) GetBorderWidth() int    { return c.borderWidth }
func (c *CircleImageViewPublic) SetFillColor(v int)     { c.fillColor = v }
func (c *CircleImageViewPublic) GetFillColor() int      { return c.fillColor }
func (c *CircleImageViewPublic) SetBorderOverlay(v bool) {
	c.borderOverlay = v
}
func (c *CircleImageViewPublic) IsBorderOverlay() bool { return c.borderOverlay }

func TestCircleImageViewPublic_BorderColorChange(t *testing.T) {
	civ := NewCircleImageViewPublic()
	civ.SetBorderColor(0xFF0000) // Color.RED
	if civ.GetBorderColor() != 0xFF0000 {
		t.Errorf("Expected border color RED (0xFF0000), got %d", civ.GetBorderColor())
	}
	civ.SetBorderColor(0x00FF00) // Color.GREEN
	if civ.GetBorderColor() != 0x00FF00 {
		t.Errorf("Expected border color GREEN (0x00FF00), got %d", civ.GetBorderColor())
	}
}

func TestCircleImageViewPublic_BorderWidthChange(t *testing.T) {
	civ := NewCircleImageViewPublic()
	civ.SetBorderWidth(8)
	if civ.GetBorderWidth() != 8 {
		t.Errorf("Expected border width 8, got %d", civ.GetBorderWidth())
	}
	civ.SetBorderWidth(0)
	if civ.GetBorderWidth() != 0 {
		t.Errorf("Expected border width 0, got %d", civ.GetBorderWidth())
	}
}

func TestCircleImageViewPublic_FillColorChange(t *testing.T) {
	civ := NewCircleImageViewPublic()
	civ.SetFillColor(0xFFFF00) // Color.YELLOW
	if civ.GetFillColor() != 0xFFFF00 {
		t.Errorf("Expected fill color YELLOW (0xFFFF00), got %d", civ.GetFillColor())
	}
	civ.SetFillColor(0x00FFFF) // Color.CYAN
	if civ.GetFillColor() != 0x00FFFF {
		t.Errorf("Expected fill color CYAN (0x00FFFF), got %d", civ.GetFillColor())
	}
}

func TestCircleImageViewPublic_BorderOverlayChange(t *testing.T) {
	civ := NewCircleImageViewPublic()
	civ.SetBorderOverlay(true)
	if !civ.IsBorderOverlay() {
		t.Errorf("Expected border overlay true, got false")
	}
	civ.SetBorderOverlay(false)
	if civ.IsBorderOverlay() {
		t.Errorf("Expected border overlay false, got true")
	}
}