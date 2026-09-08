package public_tests

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

func defaultPublicArgs() CommandLineArguments {
	return CommandLineArguments{
		MailboxFileName:          nil,
		User:                     "me",
		MaxMessages:              nil,
		ClientSecretResourcePath: "/resources/client_secret.json",
	}
}

func TestCommandLineArguments_DefaultsPublic(t *testing.T) {
	args := defaultPublicArgs()
	assert.Nil(t, args.MailboxFileName)
	assert.Equal(t, "me", args.User)
	assert.Nil(t, args.MaxMessages)
	assert.Equal(t, "/resources/client_secret.json", args.ClientSecretResourcePath)
}

func TestCommandLineArguments_SetArgumentsPublic(t *testing.T) {
	mailbox := "/var/mail"
	user := "anotheruser@domain.com"
	max := 42
	csrp := "/different/path/secret_v2.json"
	args := CommandLineArguments{
		MailboxFileName:          &mailbox,
		User:                     user,
		MaxMessages:              &max,
		ClientSecretResourcePath: csrp,
	}
	assert.Equal(t, "/var/mail", *args.MailboxFileName)
	assert.Equal(t, "anotheruser@domain.com", args.User)
	assert.Equal(t, 42, *args.MaxMessages)
	assert.Equal(t, "/different/path/secret_v2.json", args.ClientSecretResourcePath)
}