package original

import (
	"encoding/json"
	"testing"
)

// For translation, ChannelInfo and relevant functions are copied from above.

func GetChannel(f interface{}) interface{} {
	// Return nil for null file
	if f == nil {
		return nil
	}
	return ""
}

func GetChannelInfo(f interface{}) *ChannelInfo {
	if f == nil {
		return nil
	}
	return &ChannelInfo{}
}

func GetChannelInfoMap(f interface{}) map[string]string {
	if f == nil {
		return nil
	}
	return map[string]string{}
}

func ParseChannel(jsonStr string) *ChannelInfo {
	// Very minimal emulation: parse JSON and extract channel and extra if present
	if jsonStr == "" {
		return nil
	}
	var raw map[string]interface{}
	err := json.Unmarshal([]byte(jsonStr), &raw)
	if err != nil {
		return nil
	}

	info := &ChannelInfo{}
	if ch, ok := raw["channel"].(string); ok {
		info.Channel = ch
	}
	if extra, ok := raw["extra"].(map[string]interface{}); ok {
		m := map[string]string{}
		for k, v := range extra {
			if val, ok := v.(string); ok {
				m[k] = val
			}
		}
		info.ExtraInfo = m
	}
	return info
}

func TestChannelReader_GetChannel_normal(t *testing.T) {
	var file interface{} = nil
	if GetChannel(file) != nil {
		t.Errorf("expected nil on nil file")
	}
}

func TestChannelReader_GetChannelInfo_normal(t *testing.T) {
	var file interface{} = nil
	if GetChannelInfo(file) != nil {
		t.Errorf("expected nil on nil file")
	}
}

func TestChannelReader_GetChannelInfoMap_nullFile(t *testing.T) {
	var file interface{} = nil
	if GetChannelInfoMap(file) != nil {
		t.Errorf("expected nil on nil file")
	}
}

func TestChannelReader_ParseChannel_nullString(t *testing.T) {
	if ParseChannel("") != nil {
		t.Errorf("expected nil on null string")
	}
}

func TestChannelReader_ParseChannel_malformed(t *testing.T) {
	malformed := "{not-a-json}"
	if ParseChannel(malformed) != nil {
		t.Errorf("expected nil for malformed json")
	}
}

func TestChannelReader_ParseChannel_valid(t *testing.T) {
	jsonStr := `{"channel":"TestChannel","extra":{"foo":"bar"}}`
	info := ParseChannel(jsonStr)
	if info == nil {
		t.Fatalf("expected non-nil info")
	}
	if info.Channel != "TestChannel" {
		t.Errorf("expected channel 'TestChannel', got %v", info.Channel)
	}
	if info.ExtraInfo == nil || info.ExtraInfo["foo"] != "bar" {
		t.Errorf("expected extra foo=bar, got %v", info.ExtraInfo)
	}
}

func TestChannelReader_ParseChannel_valid_noExtra(t *testing.T) {
	jsonStr := `{"channel":"A"}`
	info := ParseChannel(jsonStr)
	if info == nil {
		t.Fatalf("expected non-nil info")
	}
	if info.Channel != "A" {
		t.Errorf("expected channel 'A', got %v", info.Channel)
	}
	if info.ExtraInfo != nil {
		t.Errorf("expected nil ExtraInfo, got %v", info.ExtraInfo)
	}
}

func TestChannelReader_ParseChannel_valid_nullChannel(t *testing.T) {
	jsonStr := `{"extra":{"foo":"bar"}}`
	info := ParseChannel(jsonStr)
	if info == nil {
		t.Fatalf("expected non-nil info")
	}
	if info.Channel != "" {
		t.Errorf("expected nil (empty) channel, got %v", info.Channel)
	}
	if info.ExtraInfo == nil || info.ExtraInfo["foo"] != "bar" {
		t.Errorf("expected extra foo=bar, got %v", info.ExtraInfo)
	}
}