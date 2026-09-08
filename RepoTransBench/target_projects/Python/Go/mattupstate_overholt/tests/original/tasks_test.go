package original

import (
	"strings"
	"testing"
	"mattupstate_overholt/overholt/tasks"
	"bytes"
	"fmt"
	"io"
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

func TestSendManagerAddedEmailPrints(t *testing.T) {
	output := captureStdout(func() {
		tasks.SendManagerAddedEmail("user1@example.com", "user2@example.com")
	})
	if !strings.Contains(output, "sending manager added email") {
		t.Errorf("Expected output to contain 'sending manager added email', got '%s'", output)
	}
}

func TestSendManagerRemovedEmailPrints(t *testing.T) {
	output := captureStdout(func() {
		tasks.SendManagerRemovedEmail("user3@example.com")
	})
	if !strings.Contains(output, "sending manager removed email") {
		t.Errorf("Expected output to contain 'sending manager removed email', got '%s'", output)
	}
}