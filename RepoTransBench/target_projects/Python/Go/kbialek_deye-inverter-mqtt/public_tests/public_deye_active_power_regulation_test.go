package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulated State enum
type ActivePowerRegulationState int

const (
	Idle ActivePowerRegulationState = iota
	SetpointChanged
	Applied
)

type ActivePowerRegulationStateMachine struct {
	state            ActivePowerRegulationState
	targetActivePower *float64
}

func NewActivePowerRegulationStateMachine() *ActivePowerRegulationStateMachine {
	return &ActivePowerRegulationStateMachine{
		state: Idle,
	}
}

func (m *ActivePowerRegulationStateMachine) SetTargetActivePower(val float64) {
	m.targetActivePower = &val
	m.state = SetpointChanged
}

func (m *ActivePowerRegulationStateMachine) ApplySetpoint() {
	m.state = Applied
}

func (m *ActivePowerRegulationStateMachine) Reset() {
	m.state = Idle
	m.targetActivePower = nil
}

func TestInitialState(t *testing.T) {
	m := NewActivePowerRegulationStateMachine()
	assert.Equal(t, Idle, m.state)
}

func TestSetTargetActivePowerSwitchesState(t *testing.T) {
	m := NewActivePowerRegulationStateMachine()
	m.SetTargetActivePower(524.5)
	assert.Equal(t, 524.5, *m.targetActivePower)
	assert.Equal(t, SetpointChanged, m.state)
}

func TestStateGoesToApplied(t *testing.T) {
	m := NewActivePowerRegulationStateMachine()
	m.SetTargetActivePower(802.1)
	m.ApplySetpoint()
	assert.Equal(t, Applied, m.state)
	assert.Equal(t, 802.1, *m.targetActivePower)
}

func TestResetRevertsToIdle(t *testing.T) {
	m := NewActivePowerRegulationStateMachine()
	m.SetTargetActivePower(301.0)
	m.Reset()
	assert.Equal(t, Idle, m.state)
	assert.Nil(t, m.targetActivePower)
}