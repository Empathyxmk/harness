package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type FlagsModule struct {
	Args *CommandLineArguments
}

func NewFlagsModule(args *CommandLineArguments) *FlagsModule {
	return &FlagsModule{Args: args}
}

func (fm *FlagsModule) Inject() *CommandLineArguments {
	return fm.Args
}

func TestFlagsModuleProvidesDifferentInstance(t *testing.T) {
	mailbox := "/opt/mailbox"
	user := "pubuser@domain.com"
	max := 109
	csrp := "/foo/bar/client_secret_new.json"
	args := CommandLineArguments{
		MailboxFileName:          &mailbox,
		User:                     user,
		MaxMessages:              &max,
		ClientSecretResourcePath: csrp,
	}
	module := NewFlagsModule(&args)
	injected := module.Inject()
	assert.Equal(t, &args, injected)
	assert.Equal(t, "/opt/mailbox", *injected.MailboxFileName)
	assert.Equal(t, "pubuser@domain.com", injected.User)
	assert.Equal(t, 109, *injected.MaxMessages)
	assert.Equal(t, "/foo/bar/client_secret_new.json", injected.ClientSecretResourcePath)
}