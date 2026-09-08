package original

import (
	"fmt"
	"testing"
)

// -- The following stub types mimic the Channel class and logic for translation purposes --

type Channel struct {
	channelName string
	obj         interface{}
}

func NewChannel(name string, v ...interface{}) *Channel {
	c := &Channel{channelName: name}
	if len(v) == 1 {
		switch v[0].(type) {
		case string, int:
			c.obj = v[0]
		}
	}
	if len(v) == 2 {
		// Possibly (int, string) or (string, string)
		c.obj = v[1]
	}
	return c
}
func (c *Channel) GetChannelName() string { return c.channelName }
func (c *Channel) SetChannelName(name string) { c.channelName = name }
func (c *Channel) SetObj(obj interface{}) { c.obj = obj }
func (c *Channel) GetObj() interface{} { return c.obj }
func (c *Channel) String() string {
	return fmt.Sprintf("Channel{channelName='%s', obj=%v}", c.channelName, c.obj)
}

func TestChannel_ConstructorsAndGetters(t *testing.T) {
	c1 := NewChannel("News")
	if c1.GetChannelName() != "News" {
		t.Errorf("Expected 'News', got '%s'", c1.GetChannelName())
	}

	c2 := NewChannel("Fun", 2, "extra")
	if c2.GetChannelName() != "Fun" {
		t.Errorf("Expected 'Fun', got '%s'", c2.GetChannelName())
	}
	if c2.GetObj() != "extra" {
		t.Errorf("Expected obj 'extra', got '%v'", c2.GetObj())
	}

	c3 := NewChannel("Sports", 3)
	if c3.GetChannelName() != "Sports" {
		t.Errorf("Expected 'Sports', got '%s'", c3.GetChannelName())
	}

	c4 := NewChannel("Games", "objval")
	if c4.GetChannelName() != "Games" {
		t.Errorf("Expected 'Games', got '%s'", c4.GetChannelName())
	}
	if c4.GetObj() != "objval" {
		t.Errorf("Expected obj 'objval', got '%v'", c4.GetObj())
	}
}

func TestChannel_Setters(t *testing.T) {
	c := NewChannel("Initial")
	c.SetChannelName("Changed")
	c.SetObj(1001)
	if c.GetChannelName() != "Changed" {
		t.Errorf("Expected 'Changed', got '%s'", c.GetChannelName())
	}
	if c.GetObj() != 1001 {
		t.Errorf("Expected obj 1001, got '%v'", c.GetObj())
	}
}

func TestChannel_ToString(t *testing.T) {
	c := NewChannel("Stringy", "val")
	s := c.String()
	if s == "" {
		t.Error("Expected non-empty string")
	}
	if !contains(s, "channelName='Stringy'") {
		t.Errorf("Expected substring channelName='Stringy', got '%s'", s)
	}
	if !contains(s, "obj=val") {
		t.Errorf("Expected substring obj=val, got '%s'", s)
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || (len(s) > len(substr) && func() bool {
		for i := 0; i+len(substr) <= len(s); i++ {
			if s[i:i+len(substr)] == substr {
				return true
			}
		}
		return false
	}()))
}