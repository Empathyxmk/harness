package original

import (
	"testing"
)

func TestGpGroupVars(t *testing.T) {
	gpVars := map[string]string{"gp_not_overridden": "gp"}
	if gpVars["gp_not_overridden"] != "gp" {
		t.Error("gp group var not as expected")
	}
}

func TestParentGroupVars(t *testing.T) {
	pVars := map[string]string{
		"parent_not_overridden":     "parent",
		"gp_overridden_in_parent":   "x",
	}
	if pVars["parent_not_overridden"] != "parent" {
		t.Error("parent_not_overridden value wrong")
	}
}

func TestHostVars(t *testing.T) {
	hVars := map[string]string{
		"gp_overridden_in_child":     "child",
		"parent_overridden_in_child": "child",
		"child_only":                 "child",
	}
	if hVars["gp_overridden_in_child"] != "child" {
		t.Error("gp_overridden_in_child not child")
	}
	if hVars["parent_overridden_in_child"] != "child" {
		t.Error("parent_overridden_in_child not child")
	}
	if hVars["child_only"] != "child" {
		t.Error("child_only not child")
	}
}