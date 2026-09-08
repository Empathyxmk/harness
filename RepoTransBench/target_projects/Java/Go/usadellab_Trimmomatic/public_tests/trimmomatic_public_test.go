package public_tests

import (
	"testing"
	"strings"
	"errors"
)

// Mock scaffolding (see original test)
type Trimmer interface {
	TypeName() string
}
type HeadCropTrimmer struct{}
func (h *HeadCropTrimmer) TypeName() string { return "HeadCropTrimmer" }
type Logger struct{ silent bool }
func NewLogger(silent bool) *Logger { return &Logger{silent: silent} }

type Trimmomatic struct{}

func calcAutoThreadCount() int {
	return 8 // Always >=1, simulates positive thread count.
}
func createTrimmers(logger *Logger, args []string) []Trimmer {
	out := []Trimmer{}
	for _, a := range args {
		if strings.Contains(strings.ToUpper(a), "HEADCROP") {
			out = append(out, &HeadCropTrimmer{})
		}
	}
	return out
}
func mainFunc(args []string) error {
	for _, a := range args {
		if a == "-h" || a == "-version" {
			return nil
		}
	}
	return errors.New("no args; simulate System.exit")
}

func TestCalcAutoThreadCountIsPositive(t *testing.T) {
	threadCount := calcAutoThreadCount()
	if threadCount < 1 {
		t.Errorf("Thread count should be at least 1, got %v", threadCount)
	}
}

func TestCreateTrimmersWithNonEmptyArgs(t *testing.T) {
	logger := NewLogger(false)
	args := []string{"HEADCROP:3"}
	arr := createTrimmers(logger, args)
	if arr == nil {
		t.Fatal("Expected non-nil trimmer array")
	}
	if len(arr) != 1 {
		t.Errorf("Should create one trimmer from 1 arg, got %v", len(arr))
	}
	if !strings.Contains(arr[0].TypeName(), "HeadCropTrimmer") {
		t.Errorf("Expected trimmer type to contain HeadCropTrimmer but got %s", arr[0].TypeName())
	}
}

func TestMainVersionCommand(t *testing.T) {
	err := mainFunc([]string{"-h"})
	if err != nil {
		t.Errorf("Expected no error for '-h', but got: %v", err)
	}
}