package public

import (
	"testing"
)

type Counter struct{ count int }

func (c *Counter) Inc() int {
	c.count++
	return c.count
}

func TestCounterInc(t *testing.T) {
	c := &Counter{}
	if c.Inc() != 1 {
		t.Errorf("Counter.Inc() 1st call = %d, want 1", c.count)
	}
	if c.Inc() != 2 {
		t.Errorf("Counter.Inc() 2nd call = %d, want 2", c.count)
	}
}