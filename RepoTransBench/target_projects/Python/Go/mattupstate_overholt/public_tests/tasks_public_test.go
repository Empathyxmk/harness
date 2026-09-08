package public_tests

import (
	"strings"
	"testing"
	"mattupstate_overholt/overholt/tasks"
	"bytes"
	"os"
)

func captureStdout(f func()) string {
	var buf bytes.Buffer
	stdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	outC := make(chan string)
	go func() {
		var b [1024]byte
		n, _ := r.Read(b[:])
		outC <- string(b[:n])
	}()

	f()
	w.Close()
	os.Stdout = stdout
	out := <-outC
	return out
}

func TestPublicSendManagerAddedEmailContent(t *testing.T) {
	output := captureStdout(func() {
		tasks.SendManagerAddedEmail("public1@example.com", "public2@example.com")
	})
	if !strings.Contains(output, "manager added email") {
		t.Errorf("Expected output to contain 'manager added email', got '%s'", output)
	}
}

func TestPublicSendManagerRemovedEmailContent(t *testing.T) {
	output := captureStdout(func() {
		tasks.SendManagerRemovedEmail("public3@example.com")
	})
	if !strings.Contains(output, "manager removed email") {
		t.Errorf("Expected output to contain 'manager removed email', got '%s'", output)
	}
}