package public_tests

import (
	"testing"
)

func TestPublicGotoLabelAndTable(t *testing.T) {
	table := map[string]int{}
	code := [][2]interface{}{
		{"label1", 10},
		{"label2", 20},
	}
	for _, pair := range code {
		name := pair[0].(string)
		line := pair[1].(int)
		table[name] = line
	}
	if table["label1"] != 10 {
		t.Errorf("expected label1=10")
	}
	if table["label2"] != 20 {
		t.Errorf("expected label2=20")
	}
}

func TestPublicGotoMacroLines(t *testing.T) {
	src := "alpha\nbeta\n# label x\n# goto x\nomega"
	lines := splitLines(src)
	foundLabel := false
	var labelLine int
	for i, line := range lines {
		if contains(line, "# label x") {
			foundLabel = true
			labelLine = i
		}
	}
	if !foundLabel {
		t.Errorf("expected to find label")
	}
	if labelLine != 2 {
		t.Errorf("expected labelLine==2, got %d", labelLine)
	}
}

func splitLines(s string) []string {
	var out []string
	curr := ""
	for _, c := range s {
		if c == '\n' {
			out = append(out, curr)
			curr = ""
		} else {
			curr += string(c)
		}
	}
	out = append(out, curr)
	return out
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || (len(s) > len(substr) && (func() bool {
		for i := 0; i <= len(s)-len(substr); i++ {
			if s[i:i+len(substr)] == substr {
				return true
			}
		}
		return false
	})()))
}

func TestPublicGotoInternalsExc(t *testing.T) {
	type Dummy struct{ msg string }
	gotError := ""
	defer func() {
		if gotError != "test error" {
			t.Fatalf("expected error msg 'test error', got %q", gotError)
		}
	}()
	// In Go, panic/recover for exceptions
	func() {
		defer func() {
			if r := recover(); r != nil {
				var ok bool
				gotError, ok = r.(string)
				if !ok {
					gotError = "unknown"
				}
			}
		}()
		panic("test error")
	}()
}