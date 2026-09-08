package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"yinjihuan_netty_im_go/tests"
)

func TestSendMessageWithDifferentContent(t *testing.T) {
	controller := tests.NewMessageController()
	receiveId := "public-user-dest"
	msg := "Hello from public test!"
	resp := controller.SendMessage(receiveId, msg)
	assert.NotNil(t, resp)
	assert.Equal(t, 200, resp.StatusCodeValue())
	body := resp.GetBody()
	assert.True(t, 
		contains(body, "success") || contains(body, "Success"),
	)
}

func TestSendMessageWithEmptyReceiveId(t *testing.T) {
	controller := tests.NewMessageController()
	receiveId := ""
	msg := "Message to no one"
	resp := controller.SendMessage(receiveId, msg)
	assert.NotNil(t, resp)
	assert.Equal(t, 200, resp.StatusCodeValue())
}

func contains(str, substr string) bool {
	return len(str) >= len(substr) && (str == substr || (len(str) > 0 && len(substr) > 0 && (str == substr || len(str) >= len(substr) && (str[:len(substr)] == substr || contains(str[1:], substr)))))
}