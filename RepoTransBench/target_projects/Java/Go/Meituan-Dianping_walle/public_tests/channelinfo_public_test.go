package public_tests

import (
	"strings"
	"testing"
)

type ChannelInfo struct {
	Channel   string
	ExtraInfo map[string]string
}

func (c *ChannelInfo) GetChannel() string {
	return c.Channel
}

func (c *ChannelInfo) GetExtraInfo() map[string]string {
	return c.ExtraInfo
}

func (c *ChannelInfo) String() string {
	// Simple string format for test purposes.
	s := c.Channel
	if c.ExtraInfo == nil {
		s += "null"
	} else {
		for k, v := range c.ExtraInfo {
			s += k + v
		}
	}
	return s
}

func TestChannelInfoPublic_GettersAndToString_public(t *testing.T) {
	info := map[string]string{"testKey": "testVal"}
	channelInfo := &ChannelInfo{"pub-channel", info}
	if channelInfo.GetChannel() != "pub-channel" {
		t.Errorf("expected 'pub-channel', got %v", channelInfo.GetChannel())
	}
	if channelInfo.GetExtraInfo()["testKey"] != "testVal" {
		t.Errorf("expected 'testVal' for 'testKey', got %v", channelInfo.GetExtraInfo()["testKey"])
	}
	s := channelInfo.String()
	if !strings.Contains(s, "pub-channel") || !strings.Contains(s, "testKey") || !strings.Contains(s, "testVal") {
		t.Errorf("string representation missing expected substrings: %v", s)
	}
}

func TestChannelInfoPublic_NullExtraInfo_public(t *testing.T) {
	channelInfo := &ChannelInfo{"pub-label", nil}
	if channelInfo.GetChannel() != "pub-label" {
		t.Errorf("expected 'pub-label', got %v", channelInfo.GetChannel())
	}
	if channelInfo.GetExtraInfo() != nil {
		t.Errorf("expected nil ExtraInfo, got %v", channelInfo.GetExtraInfo())
	}
	s := channelInfo.String()
	if !strings.Contains(s, "pub-label") || !strings.Contains(s, "null") {
		t.Errorf("string representation missing expected substrings: %v", s)
	}
}