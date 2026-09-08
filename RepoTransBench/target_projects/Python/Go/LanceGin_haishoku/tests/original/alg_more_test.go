package original

import (
	"reflect"
	"testing"
	"lancegin_haishoku/haishoku/alg"
)

func TestSortByRgbBasic(t *testing.T) {
	colors := []alg.CountColor{
		{10, alg.Color{52, 150, 70}},
		{4, alg.Color{200, 100, 30}},
		{7, alg.Color{100, 120, 140}},
	}
	result := alg.SortByRgb(colors)
	want := []alg.CountColor{
		{10, alg.Color{52, 150, 70}},
		{7, alg.Color{100, 120, 140}},
		{4, alg.Color{200, 100, 30}},
	}
	if !reflect.DeepEqual(result, want) {
		t.Errorf("SortByRgb(%v) = %v; want %v", colors, result, want)
	}
}

func TestRgbMaximumBasic(t *testing.T) {
	colors := []alg.CountColor{
		{2, alg.Color{10, 20, 30}},
		{5, alg.Color{40, 50, 60}},
		{3, alg.Color{25, 35, 45}},
	}
	result := alg.RgbMaximum(colors)
	if result.Rmax != 40 {
		t.Errorf("Rmax = %v; want 40", result.Rmax)
	}
	if result.Rmin != 10 {
		t.Errorf("Rmin = %v; want 10", result.Rmin)
	}
	if result.Gmax != 50 {
		t.Errorf("Gmax = %v; want 50", result.Gmax)
	}
	if result.Gmin != 20 {
		t.Errorf("Gmin = %v; want 20", result.Gmin)
	}
	if result.Bmax != 60 {
		t.Errorf("Bmax = %v; want 60", result.Bmax)
	}
	if result.Bmin != 30 {
		t.Errorf("Bmin = %v; want 30", result.Bmin)
	}
	if !approxEq(result.Rdvalue, 10.0) {
		t.Errorf("Rdvalue = %v; want %v", result.Rdvalue, 10.0)
	}
	if !approxEq(result.Gdvalue, 10.0) {
		t.Errorf("Gdvalue = %v; want %v", result.Gdvalue, 10.0)
	}
	if !approxEq(result.Bdvalue, 10.0) {
		t.Errorf("Bdvalue = %v; want %v", result.Bdvalue, 10.0)
	}
}

func approxEq(a, b float64) bool {
	const tol = 1e-6
	return (a-b) < tol && (b-a) < tol
}

func TestGroupByAccuracyEdge(t *testing.T) {
	colors := []alg.CountColor{
		{2, alg.Color{10, 20, 30}},
		{1, alg.Color{11, 21, 31}},
	}
	grouped := alg.GroupByAccuracy(colors, 1)
	found := 0
	for _, rgbl := range grouped {
		for _, rgl := range rgbl {
			for _, cell := range rgl {
				found += len(cell)
			}
		}
	}
	if found != 2 {
		t.Errorf("expected 2 color groups, got %v", found)
	}
}

func TestGroupByAccuracyLargeRange(t *testing.T) {
	colors := []alg.CountColor{
		{1, alg.Color{0, 0, 0}},
		{1, alg.Color{127, 127, 127}},
		{1, alg.Color{255, 255, 255}},
	}
	grouped := alg.GroupByAccuracy(colors, 3)
	out := []alg.CountColor{}
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			for k := 0; k < 3; k++ {
				out = append(out, grouped[i][j][k]...)
			}
		}
	}
	if len(out) != 3 {
		t.Errorf("expected 3 color groups, got %d", len(out))
	}
}

func TestGetWeightedMeanWeighted(t *testing.T) {
	group := []alg.CountColor{
		{10, alg.Color{100, 150, 200}},
		{10, alg.Color{110, 130, 170}},
	}
	weighted := alg.GetWeightedMean(group)
	if weighted.Count != 20 {
		t.Errorf("Weighted count = %v; want 20", weighted.Count)
	}
	if weighted.C[0] != 105 {
		t.Errorf("Weighted R = %v; want 105", weighted.C[0])
	}
	if weighted.C[1] != 140 {
		t.Errorf("Weighted G = %v; want 140", weighted.C[1])
	}
	if weighted.C[2] != 185 {
		t.Errorf("Weighted B = %v; want 185", weighted.C[2])
	}
}

func TestGetWeightedMeanSingle(t *testing.T) {
	group := []alg.CountColor{
		{1, alg.Color{1, 2, 3}},
	}
	weighted := alg.GetWeightedMean(group)
	if weighted.Count != 1 || weighted.C[0] != 1 || weighted.C[1] != 2 || weighted.C[2] != 3 {
		t.Errorf("Weighted single = %v; want (1, (1,2,3))", weighted)
	}
}

func TestGroupByAccuracyAllSameColor(t *testing.T) {
	colors := []alg.CountColor{
		{2, alg.Color{10, 20, 30}},
		{2, alg.Color{10, 20, 30}},
	}
	grouped := alg.GroupByAccuracy(colors, 3)
	found := 0
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			for k := 0; k < 3; k++ {
				found += len(grouped[i][j][k])
			}
		}
	}
	if found != 2 {
		t.Errorf("expected 2 color groups, got %d", found)
	}
}