package original

import (
	"math"
	"testing"
)

// Bezier represents a cubic Bezier curve by 4 timed points.
type Bezier struct {
	startPoint *TimedPoint
	control1   *TimedPoint
	control2   *TimedPoint
	endPoint   *TimedPoint
}

// Set assigns the 4 main curve points and returns receiver.
func (b *Bezier) Set(sp, c1, c2, ep *TimedPoint) *Bezier {
	b.startPoint = sp
	b.control1 = c1
	b.control2 = c2
	b.endPoint = ep
	return b
}

// Point computes the Bezier position at parameter t for general cubic curve.
func (b *Bezier) Point(t float64, start, c1, c2, end float64) float64 {
	mt := 1 - t
	return math.Pow(mt, 3)*start +
		3*math.Pow(mt, 2)*t*c1 +
		3*mt*math.Pow(t, 2)*c2 +
		math.Pow(t, 3)*end
}

// helper: bezierPoint for any coordinates, as in Java code (not using struct state).
func bezierPoint(t, start, c1, c2, end float64) float64 {
	mt := 1 - t
	return math.Pow(mt, 3)*start +
		3*math.Pow(mt, 2)*t*c1 +
		3*mt*math.Pow(t, 2)*c2 +
		math.Pow(t, 3)*end
}

// helper: calculates the approximate length of the Bezier curve.
func (b *Bezier) Length() float64 {
	n := 24
	var length float64
	var prevX, prevY float64
	for i := 0; i <= n; i++ {
		t := float64(i) / float64(n)
		x := bezierPoint(t, b.startPoint.x, b.control1.x, b.control2.x, b.endPoint.x)
		y := bezierPoint(t, b.startPoint.y, b.control1.y, b.control2.y, b.endPoint.y)
		if i > 0 {
			dx := x - prevX
			dy := y - prevY
			length += math.Hypot(dx, dy)
		}
		prevX, prevY = x, y
	}
	return length
}

func TestBezier_SetAndPoint(t *testing.T) {
	sp := new(TimedPoint).Set(0, 0)
	c1 := new(TimedPoint).Set(5, 5)
	c2 := new(TimedPoint).Set(10, 5)
	ep := new(TimedPoint).Set(10, 0)
	bezier := &Bezier{}
	bezier.Set(sp, c1, c2, ep)
	if bezier.startPoint != sp {
		t.Errorf("Expected startPoint=%v, got %v", sp, bezier.startPoint)
	}
	if bezier.control1 != c1 {
		t.Errorf("Expected control1=%v, got %v", c1, bezier.control1)
	}
	if bezier.control2 != c2 {
		t.Errorf("Expected control2=%v, got %v", c2, bezier.control2)
	}
	if bezier.endPoint != ep {
		t.Errorf("Expected endPoint=%v, got %v", ep, bezier.endPoint)
	}

	pointX := bezier.Point(0.5, 0, 5, 10, 10)
	if !(pointX > 0 && pointX < 10) {
		t.Errorf("Expected pointX in (0,10), got %v", pointX)
	}
	pointY := bezier.Point(0.5, 0, 5, 5, 0)
	if !(pointY >= 0 && pointY <= 5) {
		t.Errorf("Expected pointY in [0,5], got %v", pointY)
	}
}

func TestBezier_LengthStraightLine(t *testing.T) {
	sp := new(TimedPoint).Set(0, 0)
	c1 := new(TimedPoint).Set(0, 0)
	c2 := new(TimedPoint).Set(10, 0)
	ep := new(TimedPoint).Set(10, 0)
	bezier := &Bezier{}
	bezier.Set(sp, c1, c2, ep)
	length := bezier.Length()
	if !(length > 9 && length < 11) {
		t.Errorf("Length should be about 10, got: %v", length)
	}
}

func TestBezier_LengthCurved(t *testing.T) {
	sp := new(TimedPoint).Set(0, 0)
	c1 := new(TimedPoint).Set(0, 10)
	c2 := new(TimedPoint).Set(10, 10)
	ep := new(TimedPoint).Set(10, 0)
	bezier := &Bezier{}
	bezier.Set(sp, c1, c2, ep)
	length := bezier.Length()
	if length <= 10 {
		t.Errorf("Curved length should be longer than straight line, got: %v", length)
	}
}