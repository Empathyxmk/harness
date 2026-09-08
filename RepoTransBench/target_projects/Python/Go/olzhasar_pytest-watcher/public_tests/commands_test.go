package public_tests

import (
	"testing"
)

type DummyTrigger struct{}
type DummyConfig struct{}
type DummyTerminal struct{}

type AnotherDummyCommand struct {
	WasRun bool
}

func (c *AnotherDummyCommand) Run(trigger *DummyTrigger, term *DummyTerminal, config *DummyConfig) {
	c.WasRun = true
}

func getCommand9() *AnotherDummyCommand {
	return &AnotherDummyCommand{}
}

func TestRunAlternateCommand(t *testing.T) {
	trigger := &DummyTrigger{}
	config := &DummyConfig{}
	mockTerminal := &DummyTerminal{}
	command := getCommand9()

	if _, ok := interface{}(command).(*AnotherDummyCommand); !ok {
		t.Errorf("command is not AnotherDummyCommand")
	}
	if command.WasRun {
		t.Errorf("command was already run")
	}
	command.Run(trigger, mockTerminal, config)
	if !command.WasRun {
		t.Errorf("command should be run after Run")
	}
}