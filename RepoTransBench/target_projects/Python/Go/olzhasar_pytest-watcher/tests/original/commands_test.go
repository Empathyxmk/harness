package original

import (
	"testing"
)

type DummyTrigger struct{}
type DummyConfig struct{}
type DummyTerminal struct{}

type DummyCommand struct {
	Invoked bool
}

func (c *DummyCommand) Run(trigger *DummyTrigger, term *DummyTerminal, config *DummyConfig) {
	c.Invoked = true
}

type Command interface {
	Run(trigger *DummyTrigger, term *DummyTerminal, config *DummyConfig)
}

type CommandManager struct {
	registry map[string]*DummyCommand
}

func NewCommandManager() *CommandManager {
	return &CommandManager{
		registry: map[string]*DummyCommand{
			"0": &DummyCommand{},
		},
	}
}

func (m *CommandManager) GetCommand(ch string) *DummyCommand {
	return m.registry[ch]
}

func (m *CommandManager) RunCommand(ch string, trigger *DummyTrigger, term *DummyTerminal, config *DummyConfig) {
	cmd := m.GetCommand(ch)
	if cmd != nil {
		cmd.Run(trigger, term, config)
	}
}

func (m *CommandManager) RemoveCommand(ch string) {
	delete(m.registry, ch)
}

func TestRunCommand(t *testing.T) {
	manager := NewCommandManager()
	trigger := &DummyTrigger{}
	config := &DummyConfig{}
	term := &DummyTerminal{}

	cmd := manager.GetCommand("0")
	if _, ok := interface{}(cmd).(*DummyCommand); !ok {
		t.Errorf("Returned command is not DummyCommand")
	}
	if cmd.Invoked {
		t.Errorf("Command should not be invoked yet")
	}
	manager.RunCommand("0", trigger, term, config)
	if !cmd.Invoked {
		t.Errorf("Command should be invoked after RunCommand")
	}
	manager.RemoveCommand("0")
}