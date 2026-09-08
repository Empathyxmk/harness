package public_tests

import (
	"io"
	"os"
	"strings"
	"testing"
)

func TestSumIntArgsPublic(t *testing.T) {
	obj := &OverloadingCalculation2{}
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	obj.Sum(8, 13)
	w.Close()
	outBytes, _ := io.ReadAll(r)
	os.Stdout = origStdout
	if !strings.Contains(string(outBytes), "int arg method invoked") {
		t.Errorf("Expected 'int arg method invoked' in output, got %q", string(outBytes))
	}
}

func TestSumLongArgsPublic(t *testing.T) {
	obj := &OverloadingCalculation2{}
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	obj.SumInt64(13, 22)
	w.Close()
	outBytes, _ := io.ReadAll(r)
	os.Stdout = origStdout
	if !strings.Contains(string(outBytes), "long arg method invoked") {
		t.Errorf("Expected 'long arg method invoked' in output, got %q", string(outBytes))
	}
}