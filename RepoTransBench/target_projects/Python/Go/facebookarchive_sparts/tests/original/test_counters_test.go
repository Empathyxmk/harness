package original

import (
	"strconv"
	"testing"
)

type SumCounter struct {
	val float64
}

func (c *SumCounter) Get() float64      { return c.val }
func (c *SumCounter) Increment()        { c.val += 1 }
func (c *SumCounter) IncrementBy(x int) { c.val += float64(x) }
func (c *SumCounter) Add(x int)         { c.val += float64(x) }
func (c *SumCounter) Reset(f float64)   { c.val = f }

func TestSum(t *testing.T) {
	c := &SumCounter{}
	if c.Get() != 0.0 {
		t.Errorf("expect 0.0, got %v", c.Get())
	}
	c.Increment()
	if c.Get() != 1.0 {
		t.Errorf("expect 1.0, got %v", c.Get())
	}
	c.IncrementBy(10)
	if c.Get() != 11.0 {
		t.Errorf("expect 11.0, got %v", c.Get())
	}
	c.Add(10)
	if c.Get() != 21.0 {
		t.Errorf("expect 21.0, got %v", c.Get())
	}
	ival := int(c.Get())
	if ival != 21 {
		t.Errorf("int: want 21 got %d", ival)
	}
	fval := float64(c.Get())
	if fval != 21.0 {
		t.Errorf("float: want 21.0 got %f", fval)
	}
	sval := strconv.FormatFloat(c.Get(), 'f', 1, 64)
	if sval != "21.0" {
		t.Errorf("str: want 21.0 got %s", sval)
	}
	c.Reset(0.5)
	if float64(c.Get()) != 0.5 {
		t.Errorf("reset: want 0.5 got %f", c.Get())
	}
}