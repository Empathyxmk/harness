package original

import (
	"math"
	"testing"
)

// Constants and helper base for motion tests.
const (
	SMALL_DELTA  = 0.000001
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 500
)

// Point represents a point in 2D (replacement for java.awt.Point)
type Point struct {
	X int
	Y int
}

// Equals checks if two points are equal within a tolerance for float comparison
func (p Point) Equals(other Point) bool {
	return p.X == other.X && p.Y == other.Y
}

func assertPointEquals(t *testing.T, expected, actual Point) {
	if expected != actual {
		t.Fatalf("Expected point %+v but got %+v", expected, actual)
	}
}

func assertDoubleEquals(t *testing.T, expected, actual, delta float64) {
	if math.Abs(expected-actual) > delta {
		t.Fatalf("Expected %f but got %f (delta allowed %f)", expected, actual, delta)
	}
}

// MockMouse and other mocks would go here...
// For concise demonstration, a minimal mouse struct
type MockMouse struct {
	x, y int
	path []Point
}

func (m *MockMouse) MouseMove(x, y int) {
	m.x = x
	m.y = y
	m.path = append(m.path, Point{x, y})
}

func (m *MockMouse) GetMousePosition() Point {
	return Point{m.x, m.y}
}

func (m *MockMouse) GetMouseMovements() []Point {
	return append([]Point{}, m.path...)
}

// Helper to reset the mouse
func (m *MockMouse) Reset(x, y int) {
	m.x = x
	m.y = y
	m.path = []Point{Point{x, y}}
}

// assert the mouse is at position x, y
func assertMousePosition(t *testing.T, m *MockMouse, x, y int) {
	p := m.GetMousePosition()
	if math.Abs(float64(p.X)-float64(x)) > SMALL_DELTA || math.Abs(float64(p.Y)-float64(y)) > SMALL_DELTA {
		t.Fatalf("Mouse position is (%v, %v), expected (%v, %v)", p.X, p.Y, x, y)
	}
}