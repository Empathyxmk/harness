package original

import (
	"reflect"
	"testing"
)

// Test that SendMessage stores the correct message
func TestSendMessageStoresMessage(t *testing.T) {
	client := NewFakeClient()
	payload := map[string]interface{}{"foo": "bar"}
	uniqueID := "12345"
	client.SendMessage("request", "ssap://com.webos.test/uri", payload, uniqueID, nil, false)
	expected := map[string]interface{}{
		"type":   "request",
		"uri":    "ssap://com.webos.test/uri",
		"id":     uniqueID,
		"payload": payload,
	}
	client.AssertSentMessage(t, expected)
}

// Test that AssertSentMessageWithoutID checks without id
func TestAssertSentMessageWithoutID(t *testing.T) {
	client := NewFakeClient()
	payload := map[string]interface{}{"a": 1}
	client.SendMessage("request", "ssap:://some.test/uri", payload, "999", nil, false)
	expected := map[string]interface{}{
		"type":   "request",
		"uri":    "ssap:://some.test/uri",
		"payload": payload,
	}
	client.AssertSentMessageWithoutID(t, expected)
}

// Test that SetupResponse sets the response for a URI
func TestSetupResponseAssigns(t *testing.T) {
	client := NewFakeClient()
	resp := map[string]interface{}{"returnValue": true, "value": 42}
	client.SetupResponse("ssap://test/uri", resp)

	got, ok := client.SubRespQueues["ssap://test/uri"]
	if !ok {
		t.Fatalf("Expected SubRespQueues to have key after SetupResponse")
	}
	expectedMsg := Message{
		"returnValue": true,
		"value":       42,
	}
	if !reflect.DeepEqual(got[0], expectedMsg) {
		t.Errorf("Expected message %v, got %v", expectedMsg, got[0])
	}
}

// Test that Subscribe adds a callback for a given id
func TestSubscribeAddsCallback(t *testing.T) {
	client := NewFakeClient()
	id := "sub1"
	called := false
	fn := func(msg Message) { called = true }
	client.Subscribe("ssap://test/uri", id, fn)
	if _, ok := client.Subscriptions[id]; !ok {
		t.Errorf("Expected subscription entry for id %s", id)
	}
	// Simulate callback call
	client.Subscriptions[id](Message{"foo": "bar"})
	if !called {
		t.Error("Expected subscription callback to set called to true")
	}
}

// Test that Unsubscribe removes a subscription
func TestUnsubscribeRemovesSubscription(t *testing.T) {
	client := NewFakeClient()
	id := "sub2"
	client.Subscriptions[id] = func(msg Message) {}
	err := client.Unsubscribe(id)
	if err != nil {
		t.Errorf("Unsubscribe returned error: %v", err)
	}
	if _, ok := client.Subscriptions[id]; ok {
		t.Errorf("Unsubscribe did not remove id %q from Subscriptions", id)
	}
}

// Test that ReceivedMessage triggers callback
func TestReceivedMessageTriggersCallback(t *testing.T) {
	client := NewFakeClient()
	triggered := false
	cb := func(msg Message) {
		triggered = true
	}
	id := "abc123"
	client.cbByReqID[id] = cb

	// Simulate a received message
	jsonMsg := `{"id": "abc123", "type": "response"}`
	client.ReceivedMessage(jsonMsg)
	if !triggered {
		t.Error("Expected callback to be triggered after ReceivedMessage")
	}
}