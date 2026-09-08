package public_tests

import "testing"

type Rect struct {
	X int
	Y int
}

func boundingBox(pts []Rect) (int, int, int, int) {
	// Minimal example, acts as stub for test structure
	minX, minY := pts[0].X, pts[0].Y
	maxX, maxY := pts[0].X, pts[0].Y
	for _, pt := range pts {
		if pt.X < minX {
			minX = pt.X
		}
		if pt.Y < minY {
			minY = pt.Y
		}
		if pt.X > maxX {
			maxX = pt.X
		}
		if pt.Y > maxY {
			maxY = pt.Y
		}
	}
	return minX, minY, maxX, maxY
}

func TestBoundingBoxRectPublic(t *testing.T) {
	pts := []Rect{{5, 7}, {25, 7}, {25, 32}, {5, 32}}
	x1, y1, x2, y2 := boundingBox(pts)
	if x1 != 5 || y1 != 7 || x2 != 25 || y2 != 32 {
		t.Errorf("Unexpected bounding box (%d,%d,%d,%d)", x1, y1, x2, y2)
	}
	pts_reorder := []Rect{{25, 32}, {25, 7}, {5, 32}, {5, 7}}
	x3, y3, x4, y4 := boundingBox(pts_reorder)
	if x3 != 5 || y3 != 7 || x4 != 25 || y4 != 32 {
		t.Errorf("Unexpected bounding box (%d,%d,%d,%d)", x3, y3, x4, y4)
	}
}

func TestBoundingBoxNegativeCoordsPublic(t *testing.T) {
	pts := []Rect{{-12, -8}, {0, -8}, {0, 2}, {-12, 2}}
	x1, y1, x2, y2 := boundingBox(pts)
	if x1 != -12 || y1 != -8 || x2 != 0 || y2 != 2 {
		t.Errorf("Unexpected bounding box with negatives: (%d,%d,%d,%d)", x1, y1, x2, y2)
	}
}