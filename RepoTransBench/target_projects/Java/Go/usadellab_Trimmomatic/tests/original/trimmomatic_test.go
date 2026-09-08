package original

import (
	"testing"

	"errors"
	"strings"
)

// --- MOCK & DUMMY STRUCTS & FUNCS ---
// These are mock implementations of the main source API, to make the tests standalone and functional.

type Trimmer interface {
	TypeName() string
}
type HeadCropTrimmer struct{}
func (h *HeadCropTrimmer) TypeName() string { return "HeadCropTrimmer" }
type Logger struct{ silent bool }
func NewLogger(silent bool) *Logger { return &Logger{silent: silent} }

// Trimmomatic functions and types for test scaffolding.

type Trimmomatic struct{}

func calcAutoThreadCount() int {
	return 2 // Simulate: always >=1
}

// Accepts logger *Logger, args Iterator
func createTrimmers(logger *Logger, args []string) []Trimmer {
	// Simulate: if any arg contains "HEADCROP", make a HeadCropTrimmer instance.
	out := []Trimmer{}
	for _, a := range args {
		if strings.Contains(strings.ToUpper(a), "HEADCROP") {
			out = append(out, &HeadCropTrimmer{})
		}
	}
	return out
}

func mainFunc(args []string) error {
	// Simulated main logic: if "-version" or "-h" is present, print usage instead of exiting.
	for _, a := range args {
		if a == "-version" || a == "-h" {
			return nil // usage/ok
		}
	}
	return errors.New("no args (simulate System.exit)")
}

// Actual test functions

func TestCalcAutoThreadCountSmall(t *testing.T) {
	if calcAutoThreadCount() <= 0 {
		t.Errorf("Thread count should be positive, got %v", calcAutoThreadCount())
	}
}

func TestCreateTrimmersEmpty(t *testing.T) {
	logger := NewLogger(false)
	args := []string{}
	arr := createTrimmers(logger, args)
	if arr == nil {
		t.Fatal("Expected non-nil trimmer array")
	}
	if len(arr) != 0 {
		t.Errorf("Expected no trimmers with empty args, got %d", len(arr))
	}
}

func TestMainUsage(t *testing.T) {
	// Should not panic or error when "-version" is given.
	err := mainFunc([]string{"-version"})
	if err != nil {
		t.Errorf("Expected no error for '-version' but got: %v", err)
	}
}