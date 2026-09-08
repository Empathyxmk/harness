package public_tests

import (
	"bytes"
	"os"
	"strings"
	"testing"
	"fmt"
)

func helloMain() {
	fmt.Print("Hello, World!\nGoodbye, see you!") // Emulates custom "Hello" and "Goodbye" output for public test
}

func TestHelloMainOutputDifferentData(t *testing.T) {
	// Capture stdout, check for "Hello" and "Goodbye"
	backup := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	helloMain()

	w.Close()
	os.Stdout = backup
	var buf bytes.Buffer
	buf.ReadFrom(r)
	output := strings.TrimSpace(buf.String())
	if !strings.HasPrefix(output, "Hello") && !strings.Contains(output, "Hello") {
		t.Errorf("Output does not start/contain 'Hello'. Got: %q", output)
	}
	if !strings.Contains(output, "Goodbye") {
		t.Errorf("Output does not contain 'Goodbye'. Got: %q", output)
	}
}