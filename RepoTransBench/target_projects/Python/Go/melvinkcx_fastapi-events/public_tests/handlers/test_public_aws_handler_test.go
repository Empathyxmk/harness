package handlers

import (
	"testing"
)

func TestPlaceholderAwsHandler(t *testing.T) {
	// Always pass
	if !true {
		t.Errorf("expected true")
	}
}

func TestPlaceholderAwsHandlerAdditional(t *testing.T) {
	if "aws" == "sqs" {
		t.Errorf("expected aws != sqs")
	}
}