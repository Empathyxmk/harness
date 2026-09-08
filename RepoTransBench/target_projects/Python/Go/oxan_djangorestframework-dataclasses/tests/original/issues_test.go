package original

import (
	"testing"
	"errors"
)

func buggyFunction(shouldFail bool) error {
	if shouldFail {
		return errors.New("bug detected")
	}
	return nil
}

func TestIssueBuggyFunctionSuccess(t *testing.T) {
	if err := buggyFunction(false); err != nil {
		t.Errorf("Expected success, got error: %v", err)
	}
}

func TestIssueBuggyFunctionFail(t *testing.T) {
	err := buggyFunction(true)
	if err == nil {
		t.Fatalf("Expected error, got nil")
	}
	if err.Error() != "bug detected" {
		t.Fatalf("Unexpected error message: %v", err)
	}
}