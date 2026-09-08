package original

import (
	"bytes"
	"math"
	"os"
	"strings"
	"testing"
)

func TestAdderMainManual(t *testing.T) {
	if got := Add(11, 11); got != 22 {
		t.Errorf("Add(11, 11) = %d; want 22", got)
	}
	if got := AddFloat(12.3, 12.6); math.Abs(got-24.9) > 1e-9 {
		t.Errorf("AddFloat(12.3, 12.6) = %f; want 24.9", got)
	}
}

func TestExampleOverloadingMainManual(t *testing.T) {
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	ExampleOverloadingMain()
	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = origStdout

	output := string(out)
	if !strings.Contains(output, "Minimum Value = 6") {
		t.Errorf("Expected output to contain 'Minimum Value = 6', got: %q", output)
	}
	if !strings.Contains(output, "Minimum Value = 7.3") {
		t.Errorf("Expected output to contain 'Minimum Value = 7.3', got: %q", output)
	}
}

func TestOverloadingCalculation2Main(t *testing.T) {
	origStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	OverloadingCalculation2Main()
	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = origStdout

	output := string(out)
	if !strings.Contains(output, "int arg method invoked") {
		t.Errorf("Expected output to contain 'int arg method invoked', got: %q", output)
	}
}