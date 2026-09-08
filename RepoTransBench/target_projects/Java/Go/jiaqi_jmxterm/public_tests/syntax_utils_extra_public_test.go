package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type FakeJavaProcessPublic struct {
	Manageable bool
	StartCalled bool
}

func (f *FakeJavaProcessPublic) IsManageable() bool {
	return f.Manageable
}
func (f *FakeJavaProcessPublic) StartManagementAgent() {
	f.StartCalled = true
	f.Manageable = true
}
func (f *FakeJavaProcessPublic) ToUrl() string {
	return "service:jmx:rmi:///jndi/rmi://127.0.0.1:321/jmxrmi"
}

type FakeJpmPublic struct {
	Proc               *FakeJavaProcessPublic
	ReturnNull         bool
	ReturnUnmanageable bool
}

func (f *FakeJpmPublic) Get(pid int) JavaProcess {
	if f.ReturnNull {
		return nil
	}
	f.Proc.Manageable = !f.ReturnUnmanageable
	return f.Proc
}

func GetUrlPublic(pid string, jpm *FakeJpmPublic) (string, error) {
	proc := jpm.Get(0)
	if proc == nil {
		return "", errors.New("NullPointerException")
	}
	if !proc.IsManageable() {
		proc.StartManagementAgent()
		if !proc.IsManageable() {
			return "", errors.New("IllegalStateException")
		}
	}
	return proc.ToUrl(), nil
}

func TestGetUrl_pid_manageable_public(t *testing.T) {
	jpm := &FakeJpmPublic{Proc: &FakeJavaProcessPublic{Manageable: true}}
	url, err := GetUrlPublic("456", jpm)
	assert.NoError(t, err)
	assert.Equal(t, "service:jmx:rmi:///jndi/rmi://127.0.0.1:321/jmxrmi", url)
}

func TestGetUrl_pid_noProcess_public(t *testing.T) {
	jpm := &FakeJpmPublic{Proc: &FakeJavaProcessPublic{}, ReturnNull: true}
	_, err := GetUrlPublic("888", jpm)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "NullPointerException")
}

func TestGetUrl_pid_startManageable_public(t *testing.T) {
	jpm := &FakeJpmPublic{Proc: &FakeJavaProcessPublic{}, ReturnUnmanageable: true}
	url, err := GetUrlPublic("999", jpm)
	assert.NoError(t, err)
	assert.True(t, jpm.Proc.StartCalled)
	assert.Equal(t, "service:jmx:rmi:///jndi/rmi://127.0.0.1:321/jmxrmi", url)
}

func TestGetUrl_pid_failsToBecomeManageable_public(t *testing.T) {
	jpm := &FakeJpmPublic{Proc: &FakeJavaProcessPublic{}, ReturnUnmanageable: true}
	jpm.Proc = &FakeJavaProcessPublic{
		Manageable: false,
	}
	origGet := jpm.Get
	jpm.Get = func(pid int) JavaProcess {
		return &struct {
			JavaProcess
		}{
			JavaProcess: &struct {
				manage bool
			}{
				manage: false,
			},
		}
	}
	_, err := GetUrlPublic("202", jpm)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "IllegalStateException")
}