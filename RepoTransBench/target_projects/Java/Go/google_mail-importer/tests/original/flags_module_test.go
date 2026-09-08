package original

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

func TestFlagsModuleBindsArguments(t *testing.T) {
	args := defaultCommandLineArguments()
	mailbox := "foo"
	args.MailboxFileName = &mailbox
	module := NewFlagsModule(&args)
	injected := module.Inject()
	assert.Equal(t, "foo", *injected.MailboxFileName)
	assert.Equal(t, &args, injected)
}