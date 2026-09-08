package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"yinjihuan_netty_im_go/tests"
)

func setup() { tests.ConnectionPoolClear() }

func TestPushAllMessage(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	tests.ConnectionPoolPutChannel("A", ch)
	controller := tests.NewMessageController()
	result := controller.PushAllMessage("HelloAll")
	assert.Equal(t, "success", result)
	writes := ch.GetWrittenMessages()
	assert.GreaterOrEqual(t, len(writes), 1)
	found := false
	for _, msg := range writes {
		if msg == "HelloAll" {
			found = true
			break
		}
	}
	assert.True(t, found)
}

func TestPushMessageToClient(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	tests.ConnectionPoolPutChannel("uniqueID", ch)
	controller := tests.NewMessageController()
	result := controller.PushAllMessageToClient("uniqueID", "HiGuy")
	assert.Equal(t, "success", result)
	writes := ch.GetWrittenMessages()
	assert.GreaterOrEqual(t, len(writes), 1)
	found := false
	for _, msg := range writes {
		if msg == "HiGuy" {
			found = true
			break
		}
	}
	assert.True(t, found)
}

func TestPushMessageToClientNotFound(t *testing.T) {
	setup()
	controller := tests.NewMessageController()
	result := controller.PushAllMessageToClient("non-existent", "msg")
	assert.Equal(t, "success", result)
}