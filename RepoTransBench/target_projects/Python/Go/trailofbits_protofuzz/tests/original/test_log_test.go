package original

import (
	"bytes"
	"log"
	"testing"
)

// Simulated logger with toggled debug
var debugEnabled = false

func setLevelDebug(enable bool) {
	debugEnabled = enable
}

func debug(msg string) {
	if debugEnabled {
		log.Print(msg)
	}
}

func TestLogDebugAndSetLevel(t *testing.T) {
	var buf bytes.Buffer
	log.SetOutput(&buf)
	defer log.SetOutput(nil)

	setLevelDebug(true)
	debug("test debug msg")
	out := buf.String()
	if want := "test debug msg"; !contains(out, want) {
		t.Errorf("Did not find debug msg in output, got: %q", out)
	}
}

func TestLogDisableDebug(t *testing.T) {
	var buf bytes.Buffer
	log.SetOutput(&buf)
	defer log.SetOutput(nil)

	setLevelDebug(false)
	debug("noapi")
	out := buf.String()
	if contains(out, "noapi") {
		t.Errorf("Should not have output when debug is disabled")
	}
}

func contains(haystack, needle string) bool {
	return bytes.Contains([]byte(haystack), []byte(needle))
}