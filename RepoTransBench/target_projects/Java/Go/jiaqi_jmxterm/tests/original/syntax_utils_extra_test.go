package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type FakeJavaProcess struct {
	Manageable bool
	StartCalled bool
}

func (f *FakeJavaProcess) IsManageable() bool {
	return f.Manageable
}
func (f *FakeJavaProcess) StartManagementAgent() {
	f.StartCalled = true
	f.Manageable = true
}
func (f *FakeJavaProcess) ToUrl() string {
	return "service:jmx:rmi:///jndi/rmi://127.0.0.1:123/jmxrmi"
}

type JavaProcess interface {
	IsManageable() bool
	StartManagementAgent()
	ToUrl() string
}

type FakeJPM struct {
	Proc               *FakeJavaProcess
	ReturnNull         bool
	ReturnUnmanageable bool
}

func (f *FakeJPM) Get(pid int) JavaProcess {
	if f.ReturnNull {
		return nil
	}
	f.Proc.Manageable = !f.ReturnUnmanageable
	return f.Proc
}

type JavaProcessManager interface {
	Get(pid int) JavaProcess
}

// Simulate SyntaxUtils.getUrl(string pid, JPM)
func GetUrl(pid string, jpm JavaProcessManager) (string, error) {
	// For simplicity, just map "pid" string to int and call jpm.Get
	// Simulates the logic in the Java test
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

func TestGetUrl_pid_manageable(t *testing.T) {
	jpm := &FakeJPM{Proc: &FakeJavaProcess{Manageable: true}}
	url, err := GetUrl("123", jpm)
	assert.NoError(t, err)
	assert.Equal(t, "service:jmx:rmi:///jndi/rmi://127.0.0.1:123/jmxrmi", url)
}

func TestGetUrl_pid_noProcess(t *testing.T) {
	jpm := &FakeJPM{Proc: &FakeJavaProcess{}, ReturnNull: true}
	_, err := GetUrl("918", jpm)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "NullPointerException")
}

func TestGetUrl_pid_startManageable(t *testing.T) {
	jpm := &FakeJPM{Proc: &FakeJavaProcess{}, ReturnUnmanageable: true}
	url, err := GetUrl("555", jpm)
	assert.NoError(t, err)
	assert.True(t, jpm.Proc.StartCalled)
	assert.Equal(t, "service:jmx:rmi:///jndi/rmi://127.0.0.1:123/jmxrmi", url)
}

func TestGetUrl_pid_failsToBecomeManageable(t *testing.T) {
	type neverManageable struct{}
	var n neverManageable
	proc := struct {
		neverManageable
	}{}
	jpm := &FakeJPM{
		Proc: &FakeJavaProcess{},
	}
	// "proc" must implement JavaProcess, but always returns mgd=false
	alwaysUnmanageable := struct {
		JavaProcess
	}{
		JavaProcess: &struct {
			manage bool
		}{
			manage: false,
		},
	}
	jpm.Proc = &FakeJavaProcess{
		Manageable: false,
		StartCalled: false,
	}
	// Patch the Get method to return a stub that never becomes manageable
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
	_, err := GetUrl("101", jpm)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "IllegalStateException")
}