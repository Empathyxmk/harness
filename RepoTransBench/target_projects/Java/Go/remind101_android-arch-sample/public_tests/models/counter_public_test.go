package models

import "testing"

type Counter struct {
	id    int
	value int
}

func (c *Counter) GetValue() int     { return c.value }
func (c *Counter) SetValue(v int)    { c.value = v }
func (c *Counter) Increment()        { c.value++ }
func (c *Counter) Decrement()        { c.value-- }
func (c *Counter) GetId() int        { return c.id }
func (c *Counter) SetId(v int)       { c.id = v }

func TestCounterPublic_IncrementPublic(t *testing.T) {
	counter := &Counter{}
	oldValue := counter.GetValue()
	counter.Increment()
	if counter.GetValue() != oldValue+1 {
		t.Errorf("Expected counter value %d, got %d", oldValue+1, counter.GetValue())
	}
}
func TestCounterPublic_DecrementPublic(t *testing.T) {
	counter := &Counter{}
	counter.SetValue(78)
	counter.Decrement()
	if counter.GetValue() != 77 {
		t.Errorf("Expected 77 after decrement, got %d", counter.GetValue())
	}
}
func TestCounterPublic_SetValueAndGetIdPublic(t *testing.T) {
	counter := &Counter{}
	counter.SetValue(1234)
	counter.SetId(13)
	if counter.GetValue() != 1234 {
		t.Errorf("Expected value 1234, got %d", counter.GetValue())
	}
	if counter.GetId() <= 0 {
		t.Errorf("Expected id > 0, got %d", counter.GetId())
	}
}