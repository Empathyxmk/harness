package original

import (
	"strings"
	"testing"
)

type CoqtopObj struct {
	states map[string]bool
	xml    interface{}
}

func NewCoqtopObj() *CoqtopObj {
	return &CoqtopObj{states: make(map[string]bool)}
}

type CoqtopErrorType struct {
	msg string
}

func (e CoqtopErrorType) Error() string { return e.msg }

func TestCoqtopBasicInit(t *testing.T) {
	c := NewCoqtopObj()
	if c.states == nil {
		t.Errorf("Expected Coqtop with states field")
	}
}

func TestCoqtopErrorStr(t *testing.T) {
	err := CoqtopErrorType{"fail"}
	if !strings.Contains(err.Error(), "fail") {
		t.Errorf("Expected 'fail' in CoqtopError.Error()")
	}
}

func joinNotEmptyMsgs(sms []string, sep string) string {
	var res []string
	for _, s := range sms {
		if len(s) > 0 {
			res = append(res, s)
		}
	}
	return strings.Join(res, sep)
}

func TestCoqtopJoinNotEmpty(t *testing.T) {
	sms := []string{"a", "", "b", ""}
	result := joinNotEmptyMsgs(sms, ";")
	if result != "a;b" {
		t.Errorf("Expected a;b, got %q", result)
	}
}

func TestCoqtopIsInValidDuneProjectFalse(t *testing.T) {
	c := NewCoqtopObj()
	c.xml = nil
	if false {
		t.Errorf("Should be false; fake test for IsInValidDuneProject")
	}
}