package public_tests

import "testing"

type Rect struct {
	X int
	Y int
}

func polygonFromBbox(bbox [4]int) []Rect {
	// Create a rectangle as per Go version
	return []Rect{
		{bbox[0], bbox[1]},
		{bbox[2], bbox[1]},
		{bbox[2], bbox[3]},
		{bbox[0], bbox[3]},
	}
}

func TestPolygonFromBboxPublic(t *testing.T) {
	bbox := [4]int{3, 4, 16, 22}
	polygon := polygonFromBbox(bbox)
	expected := []Rect{{3, 4}, {16, 4}, {16, 22}, {3, 22}}
	for i, pt := range polygon {
		if pt != expected[i] {
			t.Errorf("Polygon mismatch: got %+v want %+v", pt, expected[i])
		}
	}
}

func TestPolygonFromBboxZeroWidthHeightPublic(t *testing.T) {
	bbox := [4]int{10, 10, 10, 25}
	polygon := polygonFromBbox(bbox)
	expected := []Rect{{10, 10}, {10, 10}, {10, 25}, {10, 25}}
	for i, pt := range polygon {
		if pt != expected[i] {
			t.Errorf("Polygon mismatch: got %+v want %+v", pt, expected[i])
		}
	}
}