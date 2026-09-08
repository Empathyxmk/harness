package original

import (
	"bytes"
	"os"
	"testing"
)

type TestJavaFXRun1 struct{}

func (t *TestJavaFXRun1) Start() {
	println("JavaFXRun1")
}

func Test_TestJavaFXRun1_Main(t *testing.T) {
	// Capture stdout
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	o := &TestJavaFXRun1{}
	o.Start()
	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	buf.ReadFrom(r)
	output := buf.String()
	if output != "JavaFXRun1\n" {
		t.Errorf("Expected output 'JavaFXRun1', got: %q", output)
	}
}