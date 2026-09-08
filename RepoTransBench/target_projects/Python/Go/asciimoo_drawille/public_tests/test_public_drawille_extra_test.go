package public_tests

import (
	"os"
	"reflect"
	"testing"
)

import drawille "github.com/example/asciimoo_drawille"

// setEnv helper for monkeypatching environment variables
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

// This file merges/ensures all unique public test logic is present.

func TestGetTerminalSizeEnvPublic(t *testing.T) {
	restore := setEnv(map[string]string{
		"LINES":   "33",
		"COLUMNS": "100",
	})
	defer restore()
	width, height := drawille.GetTerminalSize()
	if width != 100 || height != 33 {
		t.Errorf("Expected (100,33), got (%d,%d)", width, height)
	}
}

func TestNormalizeTypesPublic(t *testing.T) {
	if drawille.Normalize(15) != 15 {
		t.Errorf("Normalize(15) expected 15")
	}
	if drawille.Normalize(17.8) != 18 {
		t.Errorf("Normalize(17.8) expected 18")
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic(TypeError) for Normalize([])")
		}
	}()
	_ = drawille.Normalize([]interface{}{})
}

func TestNormalizeTypesStringPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic(TypeError) for Normalize(\"xyz\")")
		}
	}()
	_ = drawille.Normalize("xyz")
}

func TestIntDefaultDictPublic(t *testing.T) {
	d := drawille.IntDefaultDict()
	if reflect.TypeOf(d).Kind() != reflect.Map {
		t.Error("IntDefaultDictPublic must return a map")
	}
	if d[222] != 0 {
		t.Errorf("Expected d[222] == 0, got %v", d[222])
	}
	d[222] += 55
	if d[222] != 55 {
		t.Errorf("Expected d[222] == 55 after adding, got %v", d[222])
	}
}

func TestGetPosPublic(t *testing.T) {
	x, y := drawille.GetPos(7, 9)
	if x != 3 || y != 2 {
		t.Errorf("GetPos(7,9) should be (3,2), got (%d,%d)", x, y)
	}
	x, y = drawille.GetPos(4.9, 15.2)
	if x != 2 || y != 3 {
		t.Errorf("GetPos(4.9,15.2) should be (2,3), got (%d,%d)", x, y)
	}
}

func TestCanvasUnsetUnknownTypePublic(t *testing.T) {
	c := drawille.NewCanvas()
	c.Set(4, 10)
	c.Chars[4][10] = []int{15, 30}
	func() {
		defer func() {
			if r := recover(); r != nil {
				t.Errorf("Unexpected panic for Canvas.Unset with []int as value: %v", r)
			}
		}()
		c.Unset(4, 10)
	}()
}

func TestCanvasSetInvalidTypePublic(t *testing.T) {
	c := drawille.NewCanvas()
	c.Chars[6][7] = 9.81
	func() {
		defer func() {
			if r := recover(); r != nil {
				t.Errorf("Unexpected panic for Canvas.Set with float: %v", r)
			}
		}()
		c.Set(6, 7)
	}()
}

func TestCanvasToggleCrossTypePublic(t *testing.T) {
	c := drawille.NewCanvas()
	c.Chars[9][12] = nil
	func() {
		defer func() {
			if r := recover(); r != nil {
				t.Errorf("Unexpected panic for Canvas.Toggle with nil: %v", r)
			}
		}()
		c.Toggle(9, 12)
	}()
}

func TestCanvasLineEndingPropertyPublic(t *testing.T) {
	c := drawille.NewCanvas()
	c.LineEnding = "LF"
	if c.LineEnding != "LF" {
		t.Errorf("Expected line ending 'LF', got '%v'", c.LineEnding)
	}
}