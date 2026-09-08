package original

import (
	"testing"
	"strings"
)

func TestGetNameOfTheMethod(t *testing.T) {
	// In Go, we can't get the function name easily; mimic display name check
	if !strings.Contains(t.Name(), "TestGetNameOfTheMethod") {
		t.Errorf("expected test name to contain 'TestGetNameOfTheMethod', got '%s'", t.Name())
	}
}

func TestGetNameOfTheMethodWithDisplayNameAnnotation(t *testing.T) {
	// In Go, function is named by its test func; mimic annotation by test name
	if !strings.Contains(t.Name(), "TestGetNameOfTheMethodWithDisplayNameAnnotation") {
		t.Errorf("expected test name to contain 'TestGetNameOfTheMethodWithDisplayNameAnnotation', got '%s'", t.Name())
	}
}