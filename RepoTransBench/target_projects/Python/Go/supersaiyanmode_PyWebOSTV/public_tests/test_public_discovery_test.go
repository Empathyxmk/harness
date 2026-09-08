package public_tests

import (
	"github.com/supersaiyanmode_PyWebOSTV/tests/original"
	"testing"
)

func TestPublicDiscoverySetupResponse(t *testing.T) {
	client := original.NewFakeClient()
	uri := "ssap://public/discover"
	resp := map[string]interface{}{"returnValue": true, "devices": 3}
	client.SetupResponse(uri, resp)

	msgs, ok := client.SubRespQueues[uri]
	if !ok || len(msgs) != 1 {
		t.Fatalf("Expected 1 response for uri, got: %v", msgs)
	}
	if msgs[0]["devices"] != float64(3) {
		t.Errorf("Expected devices=3, got: %v", msgs[0]["devices"])
	}
}