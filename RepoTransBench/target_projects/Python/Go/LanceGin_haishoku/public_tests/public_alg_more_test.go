package public_tests

import (
	"reflect"
	"testing"
	"lancegin_haishoku/haishoku/alg"
)

func TestSortColorVariation(t *testing.T) {
	hist := map[[3]int]int{
		{20, 20, 20}:    1,
		{200, 200, 200}: 3,
		{100, 100, 100}: 2,
	}
	result := alg.SortColor(hist)
	if !reflect.DeepEqual(result[0].Color, [3]int{200, 200, 200}) {
		t.Errorf("Top color not as expected: %v", result[0].Color)
	}
	if !reflect.DeepEqual(result[1].Color, [3]int{100, 100, 100}) {
		t.Errorf("Second color not as expected: %v", result[1].Color)
	}
	if !reflect.DeepEqual(result[2].Color, [3]int{20, 20, 20}) {
		t.Errorf("Third color not as expected: %v", result[2].Color)
	}
}

func TestGetColorDistinctVivid(t *testing.T) {
	base := [][3]int{
		{13, 23, 33}, {14, 23, 32}, {110, 150, 195}, {111, 150, 195}, {110, 151, 194},
	}
	res := alg.GetColor(base, 2)
	if len(res) != 2 {
		t.Fatalf("Expected 2 colors, got %d", len(res))
	}
	found := false
	for _, x := range res {
		if reflect.TypeOf(x) == reflect.TypeOf([3]int{}) {
			found = true
			break
		}
	}
	if !found {
		t.Fatal("Didn't find any [3]int color tuple in output")
	}
}