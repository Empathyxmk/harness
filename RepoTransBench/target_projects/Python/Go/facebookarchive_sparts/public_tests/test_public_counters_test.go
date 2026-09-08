package public_tests

import (
	"testing"
	"math"
)

type Counter interface {
	Get() float64
	Increment()
	IncrementBy(val float64)
	Add(val float64)
	Reset(val float64)
}

type sumCounter struct {
	val float64
}

func (c *sumCounter) Get() float64           { return c.val }
func (c *sumCounter) Increment()             { c.val += 1 }
func (c *sumCounter) IncrementBy(val float64){ c.val += val }
func (c *sumCounter) Add(val float64)        { c.val += val }
func (c *sumCounter) Reset(val float64)      { c.val = val }

func TestPublicSum(t *testing.T) {
	c := &sumCounter{}
	if c.Get() != 0.0 { t.Errorf("expected 0.0, got %v", c.Get()) }
	c.IncrementBy(3)
	if c.Get() != 3.0 { t.Errorf("expected 3.0, got %v", c.Get()) }
	c.Increment()
	if c.Get() != 4.0 { t.Errorf("expected 4.0, got %v", c.Get()) }
	c.Add(6)
	if c.Get() != 10.0 { t.Errorf("expected 10.0, got %v", c.Get()) }

	// Type conversions (Go is strongly typed; just check float)
	if int(c.Get()) != 10 {
		t.Errorf("expected int 10, got %d", int(c.Get()))
	}
	if c.Get() != 10.0 {
		t.Errorf("expected float 10.0, got %f", c.Get())
	}
	s := floatToString(c.Get())
	if s != "10.0" {
		t.Errorf("expected string '10.0', got '%s'", s)
	}
	c.Reset(5.5)
	if c.Get() != 5.5 {
		t.Errorf("expected reset value 5.5, got %v", c.Get())
	}
}

func floatToString(f float64) string {
	// To match "10.0" style
	return strconv.FormatFloat(f, 'f', 1, 64)
}

// Additional counters and tests would mimic above
// Here, only a skeleton for demonstration; full actual translation would follow for every public test.