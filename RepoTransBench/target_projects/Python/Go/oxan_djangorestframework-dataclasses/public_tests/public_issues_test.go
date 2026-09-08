package public_tests

import (
	"testing"
	"errors"
)

func PublicIssueFunc(err bool) error {
	if err {
		return errors.New("public issue error")
	}
	return nil
}

func TestPublicIssueHandled(t *testing.T) {
	if err := PublicIssueFunc(true); err == nil {
		t.Errorf("Expected error but got nil")
	}
}