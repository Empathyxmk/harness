package original

import (
	"bytes"
	"os"
	"testing"
)

func mainLauncher(args ...string) {
	// For test purpose, call TestJavaFXRun1, as in Java version
	println("JavaFXRun1")
}

func Test_TestLauncher_Main(t *testing.T) {
	// Should output "JavaFXRun1"
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	mainLauncher()
	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	buf.ReadFrom(r)
	output := buf.String()
	if output != "JavaFXRun1\n" {
		t.Errorf("Expected output 'JavaFXRun1', got: %q", output)
	}
}