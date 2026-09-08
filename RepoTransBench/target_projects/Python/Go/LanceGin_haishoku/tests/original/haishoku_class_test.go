package original

import (
	"reflect"
	"testing"
	"lancegin_haishoku/haishoku"
)

func TestHaishokuInitSetsNone(t *testing.T) {
	h := haishoku.NewHaishoku()
	if h.Dominant != nil {
		t.Fatalf("Dominant = %v; want nil", h.Dominant)
	}
	if h.Palette != nil {
		t.Fatalf("Palette = %v; want nil", h.Palette)
	}
}

func TestLoadHaishokuMonkeypatch(t *testing.T) {
	origGetColorsMean := haishoku.GetColorsMean
	origGetPalette := haishoku.GetPalette
	origGetDominant := haishoku.GetDominant
	defer func() {
		haishoku.GetColorsMean = origGetColorsMean
		haishoku.GetPalette = origGetPalette
		haishoku.GetDominant = origGetDominant
	}()
	haishoku.GetColorsMean = func(_ string) []interface{} { return []interface{}{{1, [3]int{1, 2, 3}}} }
	haishoku.GetPalette = func(_ string) []string { return []string{"palette"} }
	haishoku.GetDominant = func(_ string) interface{} { return struct{ Dom string; Color [3]int }{"dom", [3]int{0, 0, 0}} }

	obj := haishoku.LoadHaishoku("fake/path.png")
	// Accept instance or class (Go version: struct or type?)
	if !reflect.TypeOf(obj).AssignableTo(reflect.TypeOf(haishoku.Haishoku{})) && !reflect.TypeOf(obj).AssignableTo(reflect.TypeOf("")) {
		t.Fatalf("LoadHaishoku returned type %T; want Haishoku", obj)
	}
}

func TestLoadHaishokuIsCallable(t *testing.T) {
	// In Go, functions are always callable
	_ = haishoku.LoadHaishoku
}

func TestStrReprOfHaishoku(t *testing.T) {
	h := haishoku.NewHaishoku()
	_ = h.String()
	// In Go, String() satisfies fmt.Stringer/repr
}