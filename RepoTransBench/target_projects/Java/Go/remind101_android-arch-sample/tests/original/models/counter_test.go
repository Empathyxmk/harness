package models

import (
	"testing"
)

type Counter struct {
	id    int
	value int
}

func (c *Counter) SetId(id int)    { c.id = id }
func (c *Counter) GetId() int      { return c.id }
func (c *Counter) SetValue(v int)  { c.value = v }
func (c *Counter) GetValue() int   { return c.value }

func TestCounter_DefaultConstructorAndValue(t *testing.T) {
	c := &Counter{}
	if c.GetId() != 0 {
		t.Errorf("expected id to be 0, got %d", c.GetId())
	}
	if c.GetValue() != 0 {
		t.Errorf("expected value to be 0, got %d", c.GetValue())
	}
}

func TestCounter_SetAndGetId(t *testing.T) {
	c := &Counter{}
	c.SetId(123)
	if c.GetId() != 123 {
		t.Errorf("expected id 123, got %d", c.GetId())
	}
}

func TestCounter_SetAndGetValue(t *testing.T) {
	c := &Counter{}
	c.SetValue(10)
	if c.GetValue() != 10 {
		t.Errorf("expected value 10, got %d", c.GetValue())
	}
}