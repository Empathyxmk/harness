package original

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

func TestSumIntArgs(t *testing.T) {
	obj := &OverloadingCalculation2{}
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	obj.Sum(1, 2) // Should invoke int version
	w.Close()
	outBytes, _ := io.ReadAll(r)
	os.Stdout = origStdout
	if !strings.Contains(string(outBytes), "int arg method invoked") {
		t.Errorf("Expected 'int arg method invoked' in output, got %q", string(outBytes))
	}
}

func TestSumLongArgs(t *testing.T) {
	obj := &OverloadingCalculation2{}
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	obj.SumInt64(5, 6) // Should invoke long version
	w.Close()
	outBytes, _ := io.ReadAll(r)
	os.Stdout = origStdout
	if !strings.Contains(string(outBytes), "long arg method invoked") {
		t.Errorf("Expected 'long arg method invoked' in output, got %q", string(outBytes))
	}
}

// OverloadingCalculation2 struct and methods need to be implemented.