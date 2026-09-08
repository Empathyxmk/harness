package public_tests

import (
	"math"
	"testing"
	"time"
)

type TimedPoint struct {
	x         float64
	y         float64
	timestamp int64
}

func (tp *TimedPoint) Set(x, y float64) *TimedPoint {
	tp.x = x
	tp.y = y
	tp.timestamp = time.Now().UnixNano()
	return tp
}

func (tp *TimedPoint) DistanceTo(other *TimedPoint) float64 {
	dx := tp.x - other.x
	dy := tp.y - other.y
	return math.Hypot(dx, dy)
}

func (tp *TimedPoint) VelocityFrom(start *TimedPoint) float64 {
	dist := tp.DistanceTo(start)
	timeDiff := float64(tp.timestamp - start.timestamp)
	if timeDiff <= 0 {
		return dist
	}
	seconds := timeDiff / 1e9
	vel := dist / seconds
	if math.IsNaN(vel) || math.IsInf(vel, 0) {
		return 0
	}
	return vel
}

func TestTimedPoint_SetPublic(t *testing.T) {
	tp := &TimedPoint{}
	if tp.Set(-7.2, 8.19) != tp {
		t.Errorf("Expected Set to return receiver")
	}
	if math.Abs(tp.x-(-7.2)) > 0.01 {
		t.Errorf("Expected x=-7.2, got %v", tp.x)
	}
	if math.Abs(tp.y-8.19) > 0.01 {
		t.Errorf("Expected y=8.19, got %v", tp.y)
	}
}

func TestTimedPoint_DistanceToPublic(t *testing.T) {
	t1 := new(TimedPoint).Set(1, 1)
	t2 := new(TimedPoint).Set(4, 5)
	dist := t1.DistanceTo(t2)
	if math.Abs(dist-5.0) > 0.001 {
		t.Errorf("Expected distance 5.0, got %v", dist)
	}
}

func TestTimedPoint_VelocityFromPositiveDiffPublic(t *testing.T) {
	t1 := new(TimedPoint).Set(2, 3)
	time.Sleep(2 * time.Millisecond)
	t2 := new(TimedPoint).Set(7, 11)
	velocity := t2.VelocityFrom(t1)
	if !(velocity > 0) {
		t.Errorf("Expected positive velocity, got %v", velocity)
	}
}

func TestTimedPoint_VelocityFromZeroDiffPublic(t *testing.T) {
	t1 := new(TimedPoint).Set(3, 4)
	t2 := &TimedPoint{x: 6, y: 8, timestamp: t1.timestamp}
	velocity := t2.VelocityFrom(t1)
	if math.Abs(velocity-5.0) > 0.001 {
		t.Errorf("Expected velocity 5.0, got %v", velocity)
	}
}

func TestTimedPoint_VelocityNaNInfinitePublic(t *testing.T) {
	t1 := &TimedPoint{x: 10, y: 10, timestamp: 500}
	t2 := &TimedPoint{x: 10, y: 10, timestamp: 600}
	velocity := t2.VelocityFrom(t1)
	if velocity != 0 {
		t.Errorf("Expected velocity 0, got %v", velocity)
	}
}