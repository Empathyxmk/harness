package original

import (
	"testing"
)

// In real implementations, would test discovery network communication,
// here we focus on interaction with FakeClient and its data stores.

func TestDiscoverySetupResponse(t *testing.T) {
	client := NewFakeClient()
	uri := "ssap://discovery/scan"
	resp := map[string]interface{}{"returnValue": true, "found": true}
	client.SetupResponse(uri, resp)

	// Simulate getting the stored response.
	messages, ok := client.SubRespQueues[uri]
	if !ok {
		t.Fatalf("Expected responses for uri %q", uri)
	}
	if len(messages) != 1 {
		t.Fatalf("Expected 1 response, got %d", len(messages))
	}
	if messages[0]["found"] != true {
		t.Errorf("Expected message found=true, got %v", messages[0]["found"])
	}
}