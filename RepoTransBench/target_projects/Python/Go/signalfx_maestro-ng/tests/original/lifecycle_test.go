package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

// DummyService mimics a stateful component in unit lifecycle tests.
type DummyService struct {
	Enabled        bool
	State          string
	RunActionCalls []string
}

func (s *DummyService) RunAction(action string) error {
	s.RunActionCalls = append(s.RunActionCalls, action)
	switch action {
	case "start":
		if !s.Enabled {
			return errors.New("service disabled")
		}
		s.State = "running"
		return nil
	case "stop":
		s.State = "stopped"
		return nil
	default:
		s.State = "unknown_action"
		return errors.New("unknown action")
	}
}

func TestServiceStartStopLifecycle(t *testing.T) {
	// Start
	svc := &DummyService{Enabled: true, State: "created"}
	err := svc.RunAction("start")
	assert.NoError(t, err)
	assert.Equal(t, "running", svc.State)
	assert.Equal(t, []string{"start"}, svc.RunActionCalls)

	// Stop
	err = svc.RunAction("stop")
	assert.NoError(t, err)
	assert.Equal(t, "stopped", svc.State)
	assert.Equal(t, []string{"start", "stop"}, svc.RunActionCalls)
}

func TestServiceStartDisabled(t *testing.T) {
	svc := &DummyService{Enabled: false, State: "created"}
	err := svc.RunAction("start")
	assert.Error(t, err)
	assert.Equal(t, "service disabled", err.Error())
	assert.Equal(t, "created", svc.State)
	assert.Equal(t, []string{"start"}, svc.RunActionCalls)
}

func TestUnknownLifecycleAction(t *testing.T) {
	svc := &DummyService{Enabled: true, State: "created"}
	err := svc.RunAction("bogus")
	assert.Error(t, err)
	assert.Equal(t, "unknown_action", svc.State)
	assert.Equal(t, []string{"bogus"}, svc.RunActionCalls)
}

func TestDoubleStart(t *testing.T) {
	svc := &DummyService{Enabled: true, State: "created"}
	err := svc.RunAction("start")
	assert.NoError(t, err)
	// Start again (valid, but state remains running)
	err = svc.RunAction("start")
	assert.NoError(t, err)
	assert.Equal(t, "running", svc.State)
	assert.Equal(t, []string{"start", "start"}, svc.RunActionCalls)
}

func TestStopWithoutStart(t *testing.T) {
	svc := &DummyService{Enabled: true, State: "created"}
	err := svc.RunAction("stop")
	assert.NoError(t, err)
	assert.Equal(t, "stopped", svc.State)
	assert.Equal(t, []string{"stop"}, svc.RunActionCalls)
}

func TestMultipleTransitions(t *testing.T) {
	svc := &DummyService{Enabled: true, State: "created"}
	actions := []string{"start", "stop", "start", "bogus", "stop"}
	expectStates := []string{"running", "stopped", "running", "unknown_action", "stopped"}
	for idx, act := range actions {
		err := svc.RunAction(act)
		if act == "bogus" {
			assert.Error(t, err)
		} else {
			assert.NoError(t, err)
		}
		assert.Equal(t, expectStates[idx], svc.State)
	}
	assert.Equal(t, actions, svc.RunActionCalls)
}