package original

import (
	"testing"
)

import drawille "github.com/example/asciimoo_drawille"

func TestCanvasSet(t *testing.T) {
	c := drawille.NewCanvas()
	c.Set(0, 0)
	if _, ok := c.Chars[0][0]; !ok {
		t.Errorf("Canvas.Set did not set (0,0)")
	}
}

func TestCanvasUnsetEmpty(t *testing.T) {
	c := drawille.NewCanvas()
	c.Set(1, 1)
	c.Unset(1, 1)
	if len(c.Chars) != 0 {
		t.Errorf("Canvas.Unset did not empty chars map")
	}
}

func TestCanvasUnsetNonempty(t *testing.T) {
	c := drawille.NewCanvas()
	c.Set(0, 0)
	c.Set(0, 1)
	c.Unset(0, 1)
	if c.Chars[0][0] != 1 {
		t.Errorf("After unset(0,1), Chars[0][0] != 1")
	}
}

func TestCanvasClear(t *testing.T) {
	c := drawille.NewCanvas()
	c.Set(1, 1)
	c.Clear()
	if len(c.Chars) != 0 {
		t.Errorf("Canvas.Clear did not clear chars map")
	}
}

func TestCanvasToggle(t *testing.T) {
	c := drawille.NewCanvas()
	c.Toggle(0, 0)
	if v, ok := c.Chars[0][0]; !ok || v != 1 {
		t.Errorf("Toggle(0,0) did not set (0,0) to 1")
	}
	c.Toggle(0, 0)
	if len(c.Chars) != 0 {
		t.Errorf("Toggle(0,0) again did not clear the map")
	}
}

func TestCanvasSetText(t *testing.T) {
	c := drawille.NewCanvas()
	c.SetText(0, 0, "asdf")
	if c.Frame() != "asdf" {
		t.Errorf("Canvas.SetText did not set frame to 'asdf'")
	}
}

func TestCanvasFrame(t *testing.T) {
	c := drawille.NewCanvas()
	if c.Frame() != "" {
		t.Errorf("New Canvas.Frame() should be empty")
	}
	c.Set(0, 0)
	if c.Frame() != "⠁" {
		t.Errorf("Canvas with (0,0) expected frame to be '⠁', got '%s'", c.Frame())
	}
}

func TestCanvasMaxMinLimits(t *testing.T) {
	c := drawille.NewCanvas()
	c.Set(0, 0)
	if c.FrameWithBounds(2, 0, 9999, 9999) != "" {
		t.Errorf("Frame(min_x=2) must be empty")
	}
	if c.FrameWithBounds(-9999, -9999, 0, 9999) != "" {
		t.Errorf("Frame(max_x=0) must be empty")
	}
}

func TestCanvasGet(t *testing.T) {
	c := drawille.NewCanvas()
	if c.Get(0, 0) {
		t.Errorf("Canvas.Get(0,0) expected false")
	}
	c.Set(0, 0)
	if !c.Get(0, 0) {
		t.Errorf("After Canvas.Set(0,0), Canvas.Get(0,0) expected true")
	}
	if c.Get(0, 1) {
		t.Errorf("Canvas.Get(0,1) expected false")
	}
	if c.Get(1, 0) {
		t.Errorf("Canvas.Get(1,0) expected false")
	}
	if c.Get(1, 1) {
		t.Errorf("Canvas.Get(1,1) expected false")
	}
}

func TestLineSinglePixel(t *testing.T) {
	got := drawille.Line(0, 0, 0, 0)
	want := [][2]int{{0, 0}}
	if len(got) != len(want) || got[0][0] != 0 || got[0][1] != 0 {
		t.Errorf("Line(0,0,0,0) expected [0,0], got %v", got)
	}
}

func TestLineRow(t *testing.T) {
	got := drawille.Line(0, 0, 1, 0)
	want := [][2]int{{0, 0}, {1, 0}}
	if len(got) != len(want) || got[0][0] != 0 || got[1][0] != 1 {
		t.Errorf("Line(0,0,1,0) incorrect, got %v", got)
	}
}

func TestLineColumn(t *testing.T) {
	got := drawille.Line(0, 0, 0, 1)
	want := [][2]int{{0, 0}, {0, 1}}
	if len(got) != len(want) || got[1][1] != 1 {
		t.Errorf("Line(0,0,0,1) incorrect, got %v", got)
	}
}

func TestLineDiagonal(t *testing.T) {
	got := drawille.Line(0, 0, 1, 1)
	want := [][2]int{{0, 0}, {1, 1}}
	if len(got) != len(want) || got[1][0] != 1 || got[1][1] != 1 {
		t.Errorf("Line(0,0,1,1) incorrect, got %v", got)
	}
}

func TestTurtlePosition(t *testing.T) {
	tu := drawille.NewTurtle()
	if tu.PosX != 0 || tu.PosY != 0 {
		t.Errorf("Turtle initial pos (0,0), got (%v,%v)", tu.PosX, tu.PosY)
	}
	tu.Move(1, 1)
	if tu.PosX != 1 || tu.PosY != 1 {
		t.Errorf("After move(1,1), expected (1,1), got (%v,%v)", tu.PosX, tu.PosY)
	}
}

func TestTurtleRotation(t *testing.T) {
	tu := drawille.NewTurtle()
	if tu.Rotation != 0 {
		t.Errorf("Turtle rotation start at 0")
	}
	tu.Right(30)
	if tu.Rotation != 30 {
		t.Errorf("After right(30), rotation should be 30, got %v", tu.Rotation)
	}
	tu.Left(30)
	if tu.Rotation != 0 {
		t.Errorf("After left(30), rotation should be back to 0 (got %v)", tu.Rotation)
	}
}

func TestTurtleBrush(t *testing.T) {
	tu := drawille.NewTurtle()
	if tu.Get(tu.PosX, tu.PosY) {
		t.Errorf("Turtle initially has brush at start pos")
	}
	tu.Forward(1)
	if !tu.Get(0, 0) {
		t.Errorf("After Forward(1), brush not at (0,0)")
	}
	if !tu.Get(tu.PosX, tu.PosY) {
		t.Errorf("After Forward(1), brush not at turtle pos")
	}
	tu.Up()
	tu.Move(2, 0)
	if tu.Get(tu.PosX, tu.PosY) {
		t.Errorf("Brush still down after up+move")
	}
	tu.Down()
	tu.Move(3, 0)
	if !tu.Get(tu.PosX, tu.PosY) {
		t.Errorf("Brush not down after Down+Move")
	}
}