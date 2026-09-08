package public_tests

import (
	"github.com/supersaiyanmode_PyWebOSTV/tests/original"
	"reflect"
	"testing"
)

func TestPublicSendMessageStoresMessage(t *testing.T) {
	client := original.NewFakeClient()
	payload := map[string]interface{}{"foo": "bar"}
	uniqueID := "public_123"
	client.SendMessage("public_request", "ssap://com.lg.public/uri", payload, uniqueID, nil, false)
	expected := map[string]interface{}{
		"type":   "public_request",
		"uri":    "ssap://com.lg.public/uri",
		"id":     uniqueID,
		"payload": payload,
	}
	client.AssertSentMessage(t, expected)
}

func TestPublicAssertSentMessageWithoutID(t *testing.T) {
	client := original.NewFakeClient()
	payload := map[string]interface{}{"x": 7}
	client.SendMessage("command", "ssap:://public/uri", payload, "public999", nil, false)
	expected := map[string]interface{}{
		"type":   "command",
		"uri":    "ssap:://public/uri",
		"payload": payload,
	}
	client.AssertSentMessageWithoutID(t, expected)
}

// Simpler "subscribe" public test
func TestPublicSubscribeAndCallback(t *testing.T) {
	client := original.NewFakeClient()
	id := "pubsub"
	triggered := false
	client.Subscribe("ssap://public/notify", id, func(msg original.Message) {
		triggered = true
	})
	if _, ok := client.Subscriptions[id]; !ok {
		t.Fatalf("Expected Subscriptions to have %s key", id)
	}
	client.Subscriptions[id](original.Message{"hello": "world"})
	if !triggered {
		t.Error("Expected callback to set triggered")
	}
}