package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyCommand struct {
	Log strings.Builder
}

func (d *DummyCommand) Execute(commandLine string) {
	d.Log.WriteString("executed " + commandLine)
}

func TestDummyCommandExecution_public(t *testing.T) {
	cmd := &DummyCommand{}
	cmd.Execute("hello world public 123")
	assert.Contains(t, cmd.Log.String(), "public 123")
}