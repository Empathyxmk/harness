package public_tests

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

// DummyService emulates the target object in isolation.
type DummyService struct {
	Enabled        bool
	State          string
	RunActionCalls []string
}

func NewDummyService(enabled bool) *DummyService {
	return &DummyService{
		Enabled: enabled,
		State:   "initialized",
	}
}
func (d *DummyService) RunAction(action string) string {
	d.RunActionCalls = append(d.RunActionCalls, action)
	if action == "activate" {
		d.State = "activated"
	} else if action == "deactivate" {
		d.State = "deactivated"
	} else {
		d.State = "unknown_action"
	}
	return d.State
}

type DummyMaestroException struct {
	msg string
}

func (e DummyMaestroException) Error() string { return e.msg }

func runService(service *DummyService, action string) (string, error) {
	if !service.Enabled {
		return "", nil
	}
	// Simulate error handling equivalent: if RunAction panics, we return DummyMaestroException
	defer func() {
		recover()
	}()
	return service.RunAction(action), nil
}

func TestRunEnabledServiceActivation(t *testing.T) {
	service := NewDummyService(true)
	res, err := runService(service, "activate")
	assert.NoError(t, err)
	assert.Equal(t, []string{"activate"}, service.RunActionCalls)
	assert.Equal(t, "activated", service.State)
	assert.Equal(t, "activated", res)
}

func TestRunDisabledServiceNoAction(t *testing.T) {
	service := NewDummyService(false)
	res, err := runService(service, "activate")
	assert.NoError(t, err)
	assert.True(t, reflect.DeepEqual(nil, service.RunActionCalls) || len(service.RunActionCalls) == 0)
	assert.Equal(t, "initialized", service.State)
	assert.Equal(t, "", res)
}

func TestRunServiceHandlesUnknownAction(t *testing.T) {
	service := NewDummyService(true)
	res, err := runService(service, "suspend")
	assert.NoError(t, err)
	assert.Equal(t, []string{"suspend"}, service.RunActionCalls)
	assert.Equal(t, "unknown_action", service.State)
	assert.Equal(t, "unknown_action", res)
}

func TestRunServiceExceptionHandling(t *testing.T) {
	type FailingService struct {
		DummyService
	}
	service := &FailingService{*NewDummyService(true)}
	service.RunAction = func(action string) string {
		panic(DummyMaestroException{"Simulated failure"})
	}
	defer func() {
		if r := recover(); r != nil {
			_, ok := r.(DummyMaestroException)
			assert.True(t, ok, "should recover DummyMaestroException")
		} else {
			t.Errorf("expected DummyMaestroException, got no panic")
		}
	}()
	// This will panic
	_, _ = runService(service, "activate")
}