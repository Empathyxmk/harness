package original

import (
	"math"
	"testing"
	"time"
)

// TimedPoint represents a point with a timestamp.
type TimedPoint struct {
	x         float64
	y         float64
	timestamp int64 // Unix nanoseconds
}

// Set sets the coordinates and timestamp and returns itself.
func (tp *TimedPoint) Set(x, y float64) *TimedPoint {
	tp.x = x
	tp.y = y
	tp.timestamp = time.Now().UnixNano()
	return tp
}

// DistanceTo returns the Euclidean distance to another TimedPoint.
func (tp *TimedPoint) DistanceTo(other *TimedPoint) float64 {
	dx := tp.x - other.x
	dy := tp.y - other.y
	return math.Hypot(dx, dy)
}

// VelocityFrom returns the velocity (distance/delta time) from another point.
// If timestamps are the same or too close, falls back to returning distance.
func (tp *TimedPoint) VelocityFrom(start *TimedPoint) float64 {
	dist := tp.DistanceTo(start)
	timeDiff := float64(tp.timestamp - start.timestamp)
	if timeDiff <= 0 {
		return dist
	}
	// Convert nanoseconds to seconds for velocity (can use any base, as long as consistent)
	seconds := timeDiff / 1e9
	vel := dist / seconds
	if math.IsNaN(vel) || math.IsInf(vel, 0) {
		return 0
	}
	return vel
}

func TestTimedPoint_Set(t *testing.T) {
	tp := &TimedPoint{}
	if tp.Set(5, 10) != tp {
		t.Errorf("Expected Set to return receiver")
	}
	if math.Abs(tp.x-5) > 0.01 {
		t.Errorf("Expected x=5, got %v", tp.x)
	}
	if math.Abs(tp.y-10) > 0.01 {
		t.Errorf("Expected y=10, got %v", tp.y)
	}
}

func TestTimedPoint_DistanceTo(t *testing.T) {
	t1 := new(TimedPoint).Set(0, 0)
	t2 := new(TimedPoint).Set(3, 4)
	dist := t1.DistanceTo(t2)
	if math.Abs(dist-5.0) > 0.001 {
		t.Errorf("Expected distance 5.0, got %v", dist)
	}
}

func TestTimedPoint_VelocityFromPositiveDiff(t *testing.T) {
	t1 := new(TimedPoint).Set(0, 0)
	time.Sleep(2 * time.Millisecond)
	t2 := new(TimedPoint).Set(3, 4)
	velocity := t2.VelocityFrom(t1)
	if !(velocity > 0) {
		t.Errorf("Expected positive velocity, got %v", velocity)
	}
}

func TestTimedPoint_VelocityFromZeroDiff(t *testing.T) {
	t1 := new(TimedPoint).Set(0, 0)
	t2 := &TimedPoint{x: 3, y: 4, timestamp: t1.timestamp} // same timestamp
	velocity := t2.VelocityFrom(t1)
	if math.Abs(velocity-5.0) > 0.001 {
		t.Errorf("Expected velocity 5.0, got %v", velocity)
	}
}

func TestTimedPoint_VelocityNaNInfinite(t *testing.T) {
	t1 := &TimedPoint{x: 0, y: 0, timestamp: 100}
	t2 := &TimedPoint{x: 0, y: 0, timestamp: 200}
	velocity := t2.VelocityFrom(t1)
	if velocity != 0 {
		t.Errorf("Expected velocity 0, got %v", velocity)
	}
}