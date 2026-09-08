package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type CommandLineArguments struct {
	MailboxFileName           *string
	User                      string
	MaxMessages               *int
	ClientSecretResourcePath  string
}

func defaultCommandLineArguments() CommandLineArguments {
	return CommandLineArguments{
		MailboxFileName:          nil,
		User:                     "me",
		MaxMessages:              nil,
		ClientSecretResourcePath: "/resources/client_secret.json",
	}
}

func TestCommandLineArguments_Defaults(t *testing.T) {
	args := defaultCommandLineArguments()
	assert.Nil(t, args.MailboxFileName)
	assert.Equal(t, "me", args.User)
	assert.Nil(t, args.MaxMessages)
	assert.Equal(t, "/resources/client_secret.json", args.ClientSecretResourcePath)
}

func TestCommandLineArguments_SetArguments(t *testing.T) {
	mailbox := "/tmp/mail"
	user := "user@example.com"
	max := 10
	csrp := "/custom/path/secret.json"
	args := CommandLineArguments{
		MailboxFileName:          &mailbox,
		User:                     user,
		MaxMessages:              &max,
		ClientSecretResourcePath: csrp,
	}
	assert.Equal(t, "/tmp/mail", *args.MailboxFileName)
	assert.Equal(t, "user@example.com", args.User)
	assert.Equal(t, 10, *args.MaxMessages)
	assert.Equal(t, "/custom/path/secret.json", args.ClientSecretResourcePath)
}