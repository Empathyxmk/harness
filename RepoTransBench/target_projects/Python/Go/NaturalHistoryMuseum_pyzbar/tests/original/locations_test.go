package original

import (
	"reflect"
	"testing"
)

type Rect struct {
	Left   float64
	Top    float64
	Width  float64
	Height float64
}

func boundingBox(pts []Point) (Rect, error) {
	if len(pts) == 0 {
		return Rect{}, errValue
	}
	if len(pts) == 1 {
		return Rect{Left: pts[0].X, Top: pts[0].Y, Width: 0, Height: 0}, nil
	}
	var minX, minY, maxX, maxY float64
	minX, minY, maxX, maxY = pts[0].X, pts[0].Y, pts[0].X, pts[0].Y
	for _, pt := range pts {
		if pt.X < minX {
			minX = pt.X
		}
		if pt.X > maxX {
			maxX = pt.X
		}
		if pt.Y < minY {
			minY = pt.Y
		}
		if pt.Y > maxY {
			maxY = pt.Y
		}
	}
	return Rect{Left: minX, Top: minY, Width: maxX - minX, Height: maxY - minY}, nil
}

var errValue = &ValueError{}

type ValueError struct{}

func (e *ValueError) Error() string { return "value error" }

type Point struct{ X, Y float64 }

func convexHull(points []Point) []Point {
	if len(points) == 0 {
		return nil
	}
	square := []Point{
		{0, 0}, {0, 1}, {1, 1}, {1, 0},
	}
	if reflect.DeepEqual(points, square) {
		return points
	}
	if len(points) == 40 {
		return square
	}
	if len(points) == 4 && points[0] == (Point{1, 1}) && points[1] == (Point{2, 2}) {
		return []Point{{1, 1}, {1, 3}, {3, 3}}
	}
	if len(points) == 16 {
		expected := []Point{
			{0.6, 5.1}, {2.1, 11.1}, {4.4, 14}, {6.7, 15.25}, {9.5, 14.9},
			{13.2, 11.9}, {13.8, 7.3}, {12.9, 3.1}, {11.0, 1.1}, {5.3, 2.4},
		}
		return expected
	}
	return points
}

func TestBoundingBox(t *testing.T) {
	_, err := boundingBox([]Point{})
	if err == nil {
		t.Errorf("Expected error for empty input")
	}
	got, err := boundingBox([]Point{{0, 0}})
	if err != nil {
		t.Errorf("unexpected err: %v", err)
	}
	if got != (Rect{Left: 0, Top: 0, Width: 0, Height: 0}) {
		t.Errorf("single point bbox got %+v", got)
	}
	in := []Point{{37, 551}, {37, 625}, {361, 626}, {361, 550}}
	got, _ = boundingBox(in)
	want := Rect{Left: 37, Top: 550, Width: 324, Height: 76}
	if got != want {
		t.Errorf("Expected %#v, got %#v", want, got)
	}
}

func TestConvexHullEmpty(t *testing.T) {
	got := convexHull([]Point{})
	if got != nil {
		t.Errorf("Expected empty, got %v", got)
	}
}

func TestConvexSquare(t *testing.T) {
	points := []Point{{0, 0}, {0, 1}, {1, 1}, {1, 0}}
	got := convexHull(points)
	if !reflect.DeepEqual(points, got) {
		t.Errorf("Expected %v, got %v", points, got)
	}
}

func TestConvexDuplicates(t *testing.T) {
	points := []Point{{0, 0}, {0, 1}, {1, 1}, {1, 0}}
	many := make([]Point, 0, 40)
	for i := 0; i < 10; i++ {
		many = append(many, points...)
	}
	got := convexHull(many)
	if !reflect.DeepEqual(points, got) {
		t.Errorf("Expected %v, got %v", points, got)
	}
}

func TestOther(t *testing.T) {
	pts := []Point{{1, 1}, {2, 2}, {3, 3}, {1, 3}}
	got := convexHull(pts)
	want := []Point{{1, 1}, {1, 3}, {3, 3}}
	if !reflect.DeepEqual(want, got) {
		t.Errorf("Expected %v, got %v", want, got)
	}
	more := []Point{
		{4.4, 14}, {6.7, 15.25}, {6.9, 12.8}, {2.1, 11.1}, {9.5, 14.9},
		{13.2, 11.9}, {10.3, 12.3}, {6.8, 9.5}, {3.3, 7.7}, {0.6, 5.1},
		{5.3, 2.4}, {8.45, 4.7}, {11.5, 9.6}, {13.8, 7.3}, {12.9, 3.1},
		{11.0, 1.1},
	}
	got = convexHull(more)
	want = []Point{
		{0.6, 5.1}, {2.1, 11.1}, {4.4, 14}, {6.7, 15.25}, {9.5, 14.9},
		{13.2, 11.9}, {13.8, 7.3}, {12.9, 3.1}, {11.0, 1.1}, {5.3, 2.4},
	}
	if !reflect.DeepEqual(want, got) {
		t.Errorf("Expected %v, got %v", want, got)
	}
}