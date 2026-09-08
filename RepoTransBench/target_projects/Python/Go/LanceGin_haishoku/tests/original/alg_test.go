package original

import (
	"reflect"
	"testing"
	"lancegin_haishoku/haishoku/alg"
)

func TestAlg_SortByRgb(t *testing.T) {
	colors := []alg.CountColor{
		{10, alg.Color{100, 150, 200}},
		{5, alg.Color{120, 130, 140}},
		{8, alg.Color{110, 170, 130}},
		{15, alg.Color{90, 80, 210}},
		{3, alg.Color{180, 50, 60}},
		{2, alg.Color{240, 10, 20}},
	}
	result := alg.SortByRgb(colors)
	want := make([]alg.CountColor, len(colors))
	copy(want, colors)
	// sort by value of alg.Color field
	for i := 0; i < len(want)-1; i++ {
		for j := i + 1; j < len(want); j++ {
			if !alg.LessColor(want[i].C, want[j].C) && alg.LessColor(want[j].C, want[i].C) {
				want[i], want[j] = want[j], want[i]
			}
		}
	}
	if !reflect.DeepEqual(want, result) {
		t.Errorf("SortByRgb got %v, want %v", result, want)
	}
}

func TestAlg_RgbMaximum(t *testing.T) {
	colors := []alg.CountColor{
		{10, alg.Color{100, 150, 200}},
		{5, alg.Color{120, 130, 140}},
		{8, alg.Color{110, 170, 130}},
		{15, alg.Color{90, 80, 210}},
		{3, alg.Color{180, 50, 60}},
		{2, alg.Color{240, 10, 20}},
	}
	r := alg.RgbMaximum(colors)
	if r.Rmax != 240 {
		t.Errorf("Rmax = %v; want 240", r.Rmax)
	}
	if r.Rmin != 90 {
		t.Errorf("Rmin = %v; want 90", r.Rmin)
	}
	if r.Gmax != 170 {
		t.Errorf("Gmax = %v; want 170", r.Gmax)
	}
	if r.Gmin != 10 {
		t.Errorf("Gmin = %v; want 10", r.Gmin)
	}
	if r.Bmax != 210 {
		t.Errorf("Bmax = %v; want 210", r.Bmax)
	}
	if r.Bmin != 20 {
		t.Errorf("Bmin = %v; want 20", r.Bmin)
	}
}

func TestAlg_GroupByAccuracy(t *testing.T) {
	var c = []alg.CountColor{
		{10, alg.Color{100, 150, 200}},
		{5, alg.Color{120, 130, 140}},
		{8, alg.Color{110, 170, 130}},
		{15, alg.Color{90, 80, 210}},
		{3, alg.Color{180, 50, 60}},
		{2, alg.Color{240, 10, 20}},
	}
	rgb := alg.GroupByAccuracy(c, 3)
	if len(rgb) != 3 || len(rgb[0]) != 3 || len(rgb[0][0]) != 3 {
		t.Errorf("GroupByAccuracy structure not 3x3x3")
	}
}

func TestAlg_GetWeightedMean(t *testing.T) {
	group := []alg.CountColor{
		{10, alg.Color{100, 150, 200}},
		{5, alg.Color{120, 130, 140}},
	}
	wmean := alg.GetWeightedMean(group)
	if wmean.Count != 15 {
		t.Errorf("Weighted mean count = %v; want 15", wmean.Count)
	}
	if len(wmean.C) != 3 {
		t.Errorf("Weighted mean color length = %v; want 3", len(wmean.C))
	}
}

func TestAlg_GetWeightedMeanSingle(t *testing.T) {
	group := []alg.CountColor{
		{7, alg.Color{50, 60, 70}},
	}
	wmean := alg.GetWeightedMean(group)
	if wmean.Count != 7 || !reflect.DeepEqual(wmean.C, alg.Color{50, 60, 70}) {
		t.Errorf("Weighted mean for single = %v; want (7, (50,60,70))", wmean)
	}
}

func TestAlg_GetWeightedMeanZero(t *testing.T) {
	defer func() {
		if recover() == nil {
			t.Error("expected panic for zero division in empty group")
		}
	}()
	_ = alg.GetWeightedMean([]alg.CountColor{})
}