package original

import (
	"bytes"
	"fmt"
	"os"
	"strings"
	"testing"
)

// Hello main (prints "Hello, World!")
func helloMain() {
	fmt.Print("Hello, World!")
}

// Goodbye main (prints "Goodbye, cruel world")
func goodbyeMain() {
	fmt.Print("Goodbye, cruel world")
}

func captureOutput(f func()) string {
	backup := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	f()

	w.Close()
	os.Stdout = backup
	var buf bytes.Buffer
	io.Copy(&buf, r)
	return buf.String()
}

func TestHelloOutput(t *testing.T) {
	out := captureOutput(helloMain)
	if strings.TrimSpace(out) != "Hello, World!" {
		t.Errorf("Expected 'Hello, World!', got %q", out)
	}
}

func TestGoodbyeOutput(t *testing.T) {
	out := captureOutput(goodbyeMain)
	want := "Goodbye, cruel world"
	if strings.ReplaceAll(strings.TrimSpace(out), "\r", "") != want {
		t.Errorf("Expected %q, got %q", want, out)
	}
}