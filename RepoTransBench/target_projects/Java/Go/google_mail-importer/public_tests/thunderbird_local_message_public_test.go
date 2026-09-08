package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ThunderbirdLocalMessage struct {
	ID     string
	Folder string
}

func (msg *ThunderbirdLocalMessage) GetMessageID() string {
	return msg.ID
}
func (msg *ThunderbirdLocalMessage) GetFolders() []string {
	return []string{msg.Folder}
}

func TestDifferentMessageIdDefaultFolder(t *testing.T) {
	msg := &ThunderbirdLocalMessage{ID: "xyz789", Folder: "public_folder"}
	assert.Equal(t, "xyz789", msg.GetMessageID())
	assert.Contains(t, msg.GetFolders(), "public_folder")
}