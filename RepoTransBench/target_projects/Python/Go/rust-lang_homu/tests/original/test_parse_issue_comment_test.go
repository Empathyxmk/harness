package original

import (
	"strings"
	"testing"
)

// Simulated parseCommand parses "@homu: clean foo" -> ("clean", "foo")
func parseCommand(cmd string) (string, string) {
	cmd = strings.TrimSpace(cmd)
	if strings.HasPrefix(strings.ToLower(cmd), "@homu:") {
		rest := strings.TrimSpace(cmd[len("@homu:"):])
		parts := strings.SplitN(rest, " ", 2)
		if len(parts) == 2 {
			return parts[0], parts[1]
		}
		return parts[0], ""
	}
	return "", ""
}

func TestParseCommandCases(t *testing.T) {
	cmd, arg := parseCommand("@homu: retry")
	if cmd != "retry" || arg != "" {
		t.Errorf("parseCommand retry = (%q, %q), want (\"retry\", \"\")", cmd, arg)
	}
	cmd, arg = parseCommand("@homu: clean foo")
	if cmd != "clean" || arg != "foo" {
		t.Errorf("parseCommand clean foo = (%q, %q), want (\"clean\", \"foo\")", cmd, arg)
	}
}