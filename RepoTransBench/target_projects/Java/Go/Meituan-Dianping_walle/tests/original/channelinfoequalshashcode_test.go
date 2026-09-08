package original

import (
	"reflect"
	"testing"
)

// ChannelInfo is a struct with Channel and ExtraInfo.
type ChannelInfo struct {
	Channel   string
	ExtraInfo map[string]string
}

func (c *ChannelInfo) Equal(o *ChannelInfo) bool {
	if c == nil && o == nil {
		return true
	}
	if c == nil || o == nil {
		return false
	}
	if c.Channel != o.Channel {
		return false
	}
	return reflect.DeepEqual(c.ExtraInfo, o.ExtraInfo)
}

func (c *ChannelInfo) HashCode() int {
	// For demo: simplistic hash based on channel + extra.
	h := 0
	for k, v := range c.ExtraInfo {
		h += len(k) + len(v)
	}
	if c.Channel != "" {
		h += len(c.Channel)
	}
	return h
}

func TestChannelInfo_EqualsAndHashCode(t *testing.T) {
	extraA := map[string]string{"foo": "bar"}
	a := &ChannelInfo{"ch", extraA}
	b := &ChannelInfo{"ch", extraA}
	if !a.Equal(b) {
		t.Fatalf("ChannelInfo objects should be equal")
	}
	if a.HashCode() != b.HashCode() {
		t.Fatalf("ChannelInfo hash codes should be equal")
	}

	// different channel
	c := &ChannelInfo{"c2", extraA}
	if a.Equal(c) {
		t.Fatalf("ChannelInfo with different channels should not be equal")
	}

	// different extraInfo
	d := &ChannelInfo{"ch", nil}
	if a.Equal(d) {
		t.Fatalf("ChannelInfo with nil extraInfo should not be equal to non-nil extraInfo")
	}

	// null channel
	e := &ChannelInfo{"", extraA}
	f := &ChannelInfo{"", extraA}
	if !e.Equal(f) {
		t.Fatalf("ChannelInfo objects with nil (empty) channel should be equal")
	}
	if e.HashCode() != f.HashCode() {
		t.Fatalf("ChannelInfo hash codes should be equal for same data")
	}
}