package public_tests

import (
	"testing"
)

import drawille "github.com/example/asciimoo_drawille"

func TestCanvasSpeedPublic(t *testing.T) {
	canvas := drawille.NewCanvas()
	for y := 0; y < 80; y += 2 {
		canvas.Set(15, y)
	}
	buf := canvas.Frame()
	hasBraille := false
	for _, c := range buf {
		if c >= 0x2800 {
			hasBraille = true
			break
		}
	}
	if !hasBraille {
		t.Errorf("Canvas.Frame() should contain at least one braille character")
	}
	canvas.Clear()
	buf2 := canvas.Frame()
	for _, c := range buf2 {
		if c >= 0x2800 {
			t.Errorf("After Canvas.Clear(), frame should not contain any braille char")
		}
	}
}