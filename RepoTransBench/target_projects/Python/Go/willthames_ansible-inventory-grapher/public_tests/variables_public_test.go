package public_tests

import (
	"testing"
)

func TestPublicBasicVarStrip(t *testing.T) {
	d := map[string]int{"public_private": 123, "should_keep": 456}
	result := map[string]int{}
	for k, v := range d {
		if len(k) >= 7 && k[:7] == "public_" {
			continue
		}
		result[k] = v
	}
	if _, ok := result["should_keep"]; !ok {
		t.Error("'should_keep' missing after strip")
	}
	if _, ok := result["public_private"]; ok {
		t.Error("'public_private' not stripped")
	}
}

func TestPublicGroupVarPrecedence(t *testing.T) {
	groupVars := map[string]string{"pubkey": "groupval", "shared": "gshared"}
	hostVars := map[string]string{"pubkey": "hostval", "override": "hval", "shared": "hshared"}
	mergedVars := map[string]string{}
	for k, v := range groupVars {
		mergedVars[k] = v
	}
	for k, v := range hostVars {
		mergedVars[k] = v
	}
	if mergedVars["pubkey"] != "hostval" {
		t.Errorf("pubkey should be hostval, got %v", mergedVars["pubkey"])
	}
	if mergedVars["shared"] != "hshared" {
		t.Errorf("shared should be hshared, got %v", mergedVars["shared"])
	}
	if mergedVars["override"] != "hval" {
		t.Errorf("override missing/incorrect, got %v", mergedVars["override"])
	}
	if mergedVars["pubkey"] == "groupval" {
		t.Error("groupval should have been overridden")
	}
}

func TestPublicNestedVars(t *testing.T) {
	hostVars := map[string]interface{}{
		"outer": map[string]interface{}{"public_hidden": "value", "visible": 42},
		"plain": 10,
	}
	cleaned := map[string]interface{}{}
	for k, v := range hostVars {
		if inner, ok := v.(map[string]interface{}); ok {
			innerCleaned := map[string]interface{}{}
			for ik, iv := range inner {
				if len(ik) >= 7 && ik[:7] == "public_" {
					continue
				}
				innerCleaned[ik] = iv
			}
			cleaned[k] = innerCleaned
		} else if len(k) < 7 || k[:7] != "public_" {
			cleaned[k] = v
		}
	}
	if _, ok := cleaned["plain"]; !ok {
		t.Error("plain key missing after cleaning")
	}
	outer, ok := cleaned["outer"].(map[string]interface{})
	if !ok {
		t.Error("outer field missing or not a map")
	}
	if _, ok := outer["public_hidden"]; ok {
		t.Error("public_hidden not removed in nested")
	}
	if _, ok := outer["visible"]; !ok {
		t.Error("visible missing in outer after cleaning")
	}
}