package original

import (
	"bytes"
	"os"
	"testing"
)

type TestJavaFXRun0 struct{}

func (t *TestJavaFXRun0) Run() {
	println("JavaFXRun0")
}

func Test_TestJavaFXRun0_Main(t *testing.T) {
	// Capture stdout
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	o := &TestJavaFXRun0{}
	o.Run()
	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	buf.ReadFrom(r)
	output := buf.String()
	if output != "JavaFXRun0\n" {
		t.Errorf("Expected output 'JavaFXRun0', got: %q", output)
	}
}