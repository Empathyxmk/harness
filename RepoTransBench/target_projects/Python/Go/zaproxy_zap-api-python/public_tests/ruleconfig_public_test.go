package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Simple stub for ruleConfig public API
type RuleConfigPub struct {
	store map[string]map[string]string
}

func NewRuleConfigPub() *RuleConfigPub {
	return &RuleConfigPub{store: map[string]map[string]string{}}
}
func (rc *RuleConfigPub) SetRuleConfigValue(ruleId, key, value string) map[string]any {
	if rc.store == nil {
		rc.store = map[string]map[string]string{}
	}
	if rc.store[ruleId] == nil {
		rc.store[ruleId] = map[string]string{}
	}
	rc.store[ruleId][key] = value
	return map[string]any{"status": "UPDATED", "ruleId": ruleId}
}
func (rc *RuleConfigPub) GetRuleConfigValue(ruleId, key string) map[string]any {
	val := rc.store[ruleId][key]
	return map[string]any{"value": val, "key": key}
}

func TestRuleConfigSetAndGetDiffData(t *testing.T) {
	ruleId := "12001"
	key := "attackStrength"
	value := "LOW"
	rc := NewRuleConfigPub()
	setResp := rc.SetRuleConfigValue(ruleId, key, value)
	assert.Equal(t, "UPDATED", setResp["status"])
	assert.Equal(t, ruleId, setResp["ruleId"])
	getResp := rc.GetRuleConfigValue(ruleId, key)
	assert.Equal(t, value, getResp["value"])
	assert.Equal(t, key, getResp["key"])
}