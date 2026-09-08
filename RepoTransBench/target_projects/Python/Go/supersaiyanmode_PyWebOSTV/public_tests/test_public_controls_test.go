package public_tests

import (
	"github.com/supersaiyanmode_PyWebOSTV/tests/original"
	"testing"
)

func TestPublicFakeMouseClientSend(t *testing.T) {
	client := original.NewFakeMouseClient()
	msg := "MOVE"
	client.Send(msg)

	if len(client.Messages) != 1 || client.Messages[0] != msg {
		t.Errorf("Expected %q in Messages, got: %+v", msg, client.Messages)
	}
	client.AssertSentMessage(t, msg)
}