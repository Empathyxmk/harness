package tests

import (
	"testing"

	"medium-sdk-go/medium"
)

func TestClientInit(t *testing.T) {
	client := medium.NewClient("12345")
	if client.Token() != "12345" {
		t.Errorf("Expected token to be '12345', got '%s'", client.Token())
	}
}