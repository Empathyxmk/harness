package public_tests

import (
	"math"
	"testing"
)

type Bezier struct {
	startPoint *TimedPoint
	control1   *TimedPoint
	control2   *TimedPoint
	endPoint   *TimedPoint
}

func (b *Bezier) Set(sp, c1, c2, ep *TimedPoint) *Bezier {
	b.startPoint = sp
	b.control1 = c1
	b.control2 = c2
	b.endPoint = ep
	return b
}

func (b *Bezier) Point(t float64, start, c1, c2, end float64) float64 {
	mt := 1 - t
	return math.Pow(mt, 3)*start +
		3*math.Pow(mt, 2)*t*c1 +
		3*mt*math.Pow(t, 2)*c2 +
		math.Pow(t, 3)*end
}

func bezierPoint(t, start, c1, c2, end float64) float64 {
	mt := 1 - t
	return math.Pow(mt, 3)*start +
		3*math.Pow(mt, 2)*t*c1 +
		3*mt*math.Pow(t, 2)*c2 +
		math.Pow(t, 3)*end
}

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

func TestBezier_SetAndPointPublic(t *testing.T) {
	sp := new(TimedPoint).Set(2, -2)
	c1 := new(TimedPoint).Set(4, 15)
	c2 := new(TimedPoint).Set(20, 10)
	ep := new(TimedPoint).Set(25, -4)
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

	pointX := bezier.Point(0.25, 2, 4, 20, 25)
	if !(pointX > 2 && pointX < 25) {
		t.Errorf("Expected pointX in (2,25), got %v", pointX)
	}

	pointY := bezier.Point(0.75, -2, 15, 10, -4)
	if !(pointY > -4 && pointY < 15) {
		t.Errorf("Expected pointY in (-4,15), got %v", pointY)
	}
}

func TestBezier_LengthDifferentStraightLine(t *testing.T) {
	sp := new(TimedPoint).Set(10, 10)
	c1 := new(TimedPoint).Set(10, 10)
	c2 := new(TimedPoint).Set(30, 10)
	ep := new(TimedPoint).Set(30, 10)
	bezier := &Bezier{}
	bezier.Set(sp, c1, c2, ep)
	length := bezier.Length()
	if !(length > 19 && length < 21) {
		t.Errorf("Length should be about 20, got: %v", length)
	}
}

func TestBezier_LengthPublicCurved(t *testing.T) {
	sp := new(TimedPoint).Set(5, 5)
	c1 := new(TimedPoint).Set(5, 25)
	c2 := new(TimedPoint).Set(25, 25)
	ep := new(TimedPoint).Set(25, 5)
	bezier := &Bezier{}
	bezier.Set(sp, c1, c2, ep)
	length := bezier.Length()
	if length <= 20 {
		t.Errorf("Expected curved length > 20, got: %v", length)
	}
}