package public_tests

import (
	"strings"
	"testing"
)

// Public parseCommand for public tests
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

func TestParseCommandCustomCase(t *testing.T) {
	cmd, arg := parseCommand("@homu: test-queue")
	if cmd != "test-queue" || arg != "" {
		t.Errorf("parseCommand(\"@homu: test-queue\") = (%q, %q), want (\"test-queue\", \"\")", cmd, arg)
	}
}

func TestParseCommandArgumented(t *testing.T) {
	cmd, arg := parseCommand("@homu: clean bar")
	if cmd != "clean" || arg != "bar" {
		t.Errorf("parseCommand(\"@homu: clean bar\") = (%q, %q), want (\"clean\", \"bar\")", cmd, arg)
	}
}