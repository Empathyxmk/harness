package original

import (
	"testing"
)

// Test that FakeMouseClient sends and records mouse messages
func TestFakeMouseClientSendAndAssert(t *testing.T) {
	client := NewFakeMouseClient()
	msg := "CLICK"
	client.Send(msg)

	if len(client.Messages) != 1 || client.Messages[0] != msg {
		t.Errorf("Expected Messages to contain %q, got: %v", msg, client.Messages)
	}
	client.AssertSentMessage(t, msg)

	// Negative test: should fail if wrong message
	failed := false
	fakeT := &FailRecorder{failed: &failed}
	client.AssertSentMessage(fakeT, "NOT_PRESENT")
	if !failed {
		t.Error("AssertSentMessage should fail when message is missing, but it did not")
	}
}

type FailRecorder struct {
	failed *bool
}

func (f *FailRecorder) Errorf(format string, args ...interface{}) {
	*f.failed = true
}