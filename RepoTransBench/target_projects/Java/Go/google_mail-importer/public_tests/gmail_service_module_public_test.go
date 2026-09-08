package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type GmailServiceModule struct {
	MailboxName string
}

func NewGmailServiceModule(mailbox string) *GmailServiceModule {
	return &GmailServiceModule{MailboxName: mailbox}
}

func TestGmailServiceModule_ProvidesMailboxName(t *testing.T) {
	module := NewGmailServiceModule("PublicMailboxName")
	assert.Equal(t, "PublicMailboxName", module.MailboxName)
}