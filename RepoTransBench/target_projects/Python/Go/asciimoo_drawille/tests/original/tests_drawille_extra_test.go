package original

import (
	"os"
	"reflect"
	"testing"
)
import drawille "github.com/example/asciimoo_drawille"

func setEnv(kv map[string]string) func() {
	orig := make(map[string]string)
	for k := range kv {
		orig[k] = os.Getenv(k)
		os.Setenv(k, kv[k])
	}
	return func() {
		for k, v := range orig {
			os.Setenv(k, v)
		}
	}
}

func TestGetTerminalSizeEnv(t *testing.T) {
	restore := setEnv(map[string]string{
		"LINES":   "30",
		"COLUMNS": "100",
	})
	defer restore()
	width, height := drawille.GetTerminalSize()
	if width != 100 || height != 30 {
		t.Errorf("Expected (100,30), got (%d,%d)", width, height)
	}
}

func TestNormalizeTypes(t *testing.T) {
	n := drawille.Normalize(5)
	if n != 5 {
		t.Errorf("Normalize(5) expected 5, got %v", n)
	}
	n = drawille.Normalize(4.7)
	if n != 5 {
		t.Errorf("Normalize(4.7) expected 5, got %v", n)
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic(TypeError) for Normalize(\"a\")")
		}
	}()
	_ = drawille.Normalize("a")
}

func TestNormalizeTypesList(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic(TypeError) for Normalize([1,2])")
		}
	}()
	_ = drawille.Normalize([]int{1, 2})
}

func TestIntDefaultDict(t *testing.T) {
	d := drawille.IntDefaultDict()
	if reflect.TypeOf(d).Kind() != reflect.Map {
		t.Error("IntDefaultDict must return a map")
	}
	if d["x"] != 0 {
		t.Errorf(`Expected d["x"] == 0, got %v`, d["x"])
	}
}

func TestGetPos(t *testing.T) {
	if x, y := drawille.GetPos(4, 8); x != 2 || y != 2 {
		t.Errorf("GetPos(4,8) expected (2,2), got (%d,%d)", x, y)
	}
	if x, y := drawille.GetPos(1.4, 3.6); x != 0 || y != 1 {
		t.Errorf("GetPos(1.4,3.6) expected (0,1), got (%d,%d)", x, y)
	}
}

func TestCanvasUnsetUnknownType(t *testing.T) {
	c := drawille.NewCanvas()
	c.Set(0, 0)
	c.Chars[0][0] = "test"
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic in Canvas.Unset for unknown type: %v", r)
		}
	}()
	c.Unset(0, 0)
}

func TestCanvasSetInvalidType(t *testing.T) {
	c := drawille.NewCanvas()
	c.Chars[0][0] = "str"
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic in Canvas.Set with non-int value: %v", r)
		}
	}()
	c.Set(0, 0)
}

func TestCanvasToggleCrossType(t *testing.T) {
	c := drawille.NewCanvas()
	c.Chars[0][0] = "xx"
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Unexpected panic in Canvas.Toggle with cross type value: %v", r)
		}
	}()
	c.Toggle(0, 0)
}

func TestCanvasLineEndingProperty(t *testing.T) {
	c := drawille.NewCanvas()
	c.LineEnding = "END"
	if c.LineEnding != "END" {
		t.Errorf("Expected line_ending 'END', got '%v'", c.LineEnding)
	}
}