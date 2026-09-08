package public_tests

import (
	"testing"

	"medium-sdk-go/medium"
)

func TestClientInitPublic(t *testing.T) {
	client := medium.NewClient("public_token_abc")
	if client.Token() != "public_token_abc" {
		t.Errorf("Expected token to be 'public_token_abc', got '%s'", client.Token())
	}
}