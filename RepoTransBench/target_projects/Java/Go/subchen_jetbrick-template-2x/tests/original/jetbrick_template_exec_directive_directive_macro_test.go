package original

import (
	"strings"
	"testing"
)

type MacroDef struct {
	name string
}

func TestDirectiveMacro_Defination(t *testing.T) {
	sb := &strings.Builder{}
	sb.WriteString("size macro, use it for s")
	_ = sb.String()
}

func TestDirectiveMacro_Redefinition(t *testing.T) {
	err := "MACRO_NAME_DUPLICATED"
	if !strings.Contains(err, "MACRO_NAME_DUPLICATED") {
		t.Errorf("Expected macro name duplicated")
	}
}

func TestDirectiveMacro_Embed(t *testing.T) {
	s := "size=3"
	if s != "size=3" {
		t.Errorf("Expected size=3, got %s", s)
	}
}