package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ThunderbirdLocalMessage struct {
	messageID string
	folders   []string
}

func (msg *ThunderbirdLocalMessage) GetMessageID() string       { return msg.messageID }
func (msg *ThunderbirdLocalMessage) GetFolders() []string       { return msg.folders }
func (msg *ThunderbirdLocalMessage) GetRawContent() []byte      { return []byte("BODY") }
func (msg *ThunderbirdLocalMessage) GetFromHeader() string      { return "<XYZ@pdq>" }
func (msg *ThunderbirdLocalMessage) IsUnread() bool             { return true }
func (msg *ThunderbirdLocalMessage) IsStarred() bool            { return false }

func TestThunderbirdLocalMessage_GetMessageId_Normal(t *testing.T) {
	msg := ThunderbirdLocalMessage{messageID: "<XYZ@pdq>", folders: []string{"*folder*"}}
	assert.Equal(t, "<XYZ@pdq>", msg.GetMessageID())
}

func TestThunderbirdLocalMessage_GetFromHeader_Normal(t *testing.T) {
	msg := ThunderbirdLocalMessage{}
	assert.Equal(t, "<XYZ@pdq>", msg.GetFromHeader())
}

func TestThunderbirdLocalMessage_GetFolders(t *testing.T) {
	msg := ThunderbirdLocalMessage{folders: []string{"*folder*"}}
	assert.Equal(t, []string{"*folder*"}, msg.GetFolders())
}

func TestThunderbirdLocalMessage_GetRawContent(t *testing.T) {
	msg := ThunderbirdLocalMessage{}
	assert.Equal(t, []byte("BODY"), msg.GetRawContent())
}

func TestThunderbirdLocalMessage_IsUnread_True(t *testing.T) {
	msg := ThunderbirdLocalMessage{}
	assert.True(t, msg.IsUnread())
}

func TestThunderbirdLocalMessage_IsStarred_False(t *testing.T) {
	msg := ThunderbirdLocalMessage{}
	assert.False(t, msg.IsStarred())
}