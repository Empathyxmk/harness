package original

import (
	"reflect"
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

func TestChannelInfo_ConstructorAndGetters_basic(t *testing.T) {
	extra := map[string]string{"k1": "v1"}
	info := &ChannelInfo{"channelA", extra}
	if info.GetChannel() != "channelA" {
		t.Errorf("expected channelA, got %v", info.GetChannel())
	}
	if !reflect.DeepEqual(info.GetExtraInfo(), extra) {
		t.Errorf("expected %v, got %v", extra, info.GetExtraInfo())
	}
}

func TestChannelInfo_ConstructorAndGetters_nullExtra(t *testing.T) {
	info := &ChannelInfo{"abc", nil}
	if info.GetChannel() != "abc" {
		t.Errorf("expected abc, got %v", info.GetChannel())
	}
	if info.GetExtraInfo() != nil {
		t.Errorf("expected nil extraInfo, got %v", info.GetExtraInfo())
	}
}

func TestChannelInfo_ConstructorAndGetters_nullChannel(t *testing.T) {
	extra := map[string]string{}
	info := &ChannelInfo{"", extra}
	if info.GetChannel() != "" {
		t.Errorf("expected empty string for channel, got %v", info.GetChannel())
	}
	if !reflect.DeepEqual(info.GetExtraInfo(), extra) {
		t.Errorf("expected %v, got %v", extra, info.GetExtraInfo())
	}
}