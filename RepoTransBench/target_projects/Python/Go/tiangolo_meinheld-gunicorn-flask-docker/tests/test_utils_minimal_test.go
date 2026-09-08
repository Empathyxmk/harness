package tests

import (
	"strings"
	"testing"

	"github.com/example/tiangolo_meinheld-gunicorn-flask-docker/utils"
)

type DummyContainerMinimal struct {
	TopValue          map[string]interface{}
	ExecRunValue      []byte
	LogsValue         []byte
	RaiseOnTop        bool
	RaiseOnExecRun    bool
	StopCalled        bool
	RemoveCalled      bool
}

func (c *DummyContainerMinimal) Top() (map[string]interface{}, error) {
	if c.RaiseOnTop {
		return nil, &TestError{"Simulate top error"}
	}
	return c.TopValue, nil
}
func (c *DummyContainerMinimal) ExecRun(cmd string) ([]byte, error) {
	if c.RaiseOnExecRun {
		return nil, &TestError{"Simulate exec_run error"}
	}
	return c.ExecRunValue, nil
}
func (c *DummyContainerMinimal) Logs() ([]byte, error) {
	return c.LogsValue, nil
}
func (c *DummyContainerMinimal) Stop() {
	c.StopCalled = true
}
func (c *DummyContainerMinimal) Remove() {
	c.RemoveCalled = true
}
type TestError struct{ msg string }
func (e *TestError) Error() string { return e.msg }

func TestWaitForGunicornGunicornFound(t *testing.T) {
	c := &DummyContainerMinimal{
		TopValue: map[string]interface{}{
			"Processes": [][]string{{"a", "b", "c", "d", "e", "f", "g", "gunicorn -c conf.py app:app"}},
		},
	}
	result := utils.WaitForGunicorn(c, 10, 50)
	if !result {
		t.Errorf("Expected WaitForGunicorn to find gunicorn, got false")
	}
}

func TestWaitForGunicornGunicornNotfound(t *testing.T) {
	c := &DummyContainerMinimal{
		TopValue: map[string]interface{}{
			"Processes": [][]string{{"python app.py"}},
		},
	}
	result := utils.WaitForGunicorn(c, 10, 30)
	if result {
		t.Errorf("Expected WaitForGunicorn to not find gunicorn, got true")
	}
}

func TestGetConfigFromContainerSuccess(t *testing.T) {
	c := &DummyContainerMinimal{
		ExecRunValue: []byte(`{"newkey": "newvalue"}`),
	}
	r := utils.GetConfigFromContainer(c, "/etc/config.json")
	v, ok := r["newkey"]
	if !ok || v != "newvalue" {
		t.Errorf("Expected newkey with value newvalue, got %#v", r)
	}
}
func TestGetConfigFromContainerExecRunFail(t *testing.T) {
	c := &DummyContainerMinimal{
		RaiseOnExecRun: true,
	}
	r := utils.GetConfigFromContainer(c, "/fakepath")
	if r != nil {
		t.Errorf("Expected nil result when exec_run fails, got %#v", r)
	}
}

func TestPrintContainerLogsPrints(t *testing.T) {
	c := &DummyContainerMinimal{
		LogsValue: []byte("logdata"),
	}
	out := utils.PrintContainerLogs(c)
	if !strings.Contains(out, "Container logs:") {
		t.Errorf("Expected output to contain 'Container logs:', got %q", out)
	}
}

func TestCleanupContainerCallsMethods(t *testing.T) {
	c := &DummyContainerMinimal{}
	utils.CleanupContainer(c)
	if !c.StopCalled {
		t.Error("Expected Stop to be called")
	}
	if !c.RemoveCalled {
		t.Error("Expected Remove to be called")
	}
}