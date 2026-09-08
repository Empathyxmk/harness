package original

import (
	"strings"
	"testing"
)

// Minimal port of MailMerge._MailMerge__parse_instr
func parseInstr(instr string) *string {
	instr = strings.TrimSpace(instr)
	if strings.HasPrefix(instr, "MERGEFIELD") {
		rest := strings.TrimSpace(instr[len("MERGEFIELD"):])
		if len(rest) == 0 {
			return nil
		}
		if rest[0] == '"' {
			// quoted field
			rest = rest[1:]
			i := strings.Index(rest, "\"")
			if i >= 0 {
				name := rest[:i]
				return &name
			}
			return nil
		}
		// unquoted - take up to space or \
		for i, r := range rest {
			if r == ' ' || r == '\\' {
				name := rest[:i]
				return &name
			}
		}
		return &rest
	}
	return nil
}

func TestParseInstrValid(t *testing.T) {
	instr := "MERGEFIELD  somefield  \\* MERGEFORMAT"
	name := parseInstr(instr)
	if name == nil || *name != "somefield" {
		t.Fatalf("Expected 'somefield', got %v", name)
	}
}

func TestParseInstrInvalid(t *testing.T) {
	instr := "SOMETHINGELSE testing"
	name := parseInstr(instr)
	if name != nil {
		t.Fatalf("Expected nil, got %v", name)
	}
}

func TestParseInstrQuoted(t *testing.T) {
	instr := `MERGEFIELD "another field"`
	name := parseInstr(instr)
	if name == nil || *name != "another field" {
		t.Fatalf("Expected 'another field', got %v", name)
	}
}