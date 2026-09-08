package public_tests

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
		return nil, &TestError{"Dummy top error"}
	}
	return c.TopValue, nil
}
func (c *DummyContainerMinimal) ExecRun(cmd string) ([]byte, error) {
	if c.RaiseOnExecRun {
		return nil, &TestError{"Dummy exec_run error"}
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

func TestWaitForGunicornFound(t *testing.T) {
	c := &DummyContainerMinimal{
		TopValue: map[string]interface{}{
			"Processes": [][]string{{"1", "2", "3", "4", "5", "6", "7", "gunicorn -b :8080 -w 2 pubapp:app"}},
		},
	}
	result := utils.WaitForGunicorn(c, 10, 60)
	if !result {
		t.Errorf("Expected WaitForGunicorn to find gunicorn, got false")
	}
}

func TestWaitForGunicornAbsent(t *testing.T) {
	c := &DummyContainerMinimal{
		TopValue: map[string]interface{}{
			"Processes": [][]string{{"python worker.py"}},
		},
	}
	result := utils.WaitForGunicorn(c, 10, 30)
	if result {
		t.Errorf("Expected WaitForGunicorn to not find gunicorn, got true")
	}
}

func TestGetConfigFromContainerOk(t *testing.T) {
	c := &DummyContainerMinimal{
		ExecRunValue: []byte(`{"publickey":"publicvalue"}`),
	}
	r := utils.GetConfigFromContainer(c, "/myconf.json")
	v, ok := r["publickey"]
	if !ok || v != "publicvalue" {
		t.Errorf("Expected publickey with value publicvalue, got %#v", r)
	}
}
func TestGetConfigFromContainerExecRunFails(t *testing.T) {
	c := &DummyContainerMinimal{RaiseOnExecRun: true}
	r := utils.GetConfigFromContainer(c, "/notarealpath")
	if r != nil {
		t.Errorf("Expected nil result when exec_run fails, got %#v", r)
	}
}

func TestPrintContainerLogsOutput(t *testing.T) {
	c := &DummyContainerMinimal{LogsValue: []byte("publiclog")}
	out := utils.PrintContainerLogs(c)
	if !strings.Contains(out, "Container logs:") {
		t.Errorf("Expected output to contain 'Container logs:', got %q", out)
	}
}

func TestCleanupContainerStopsAndRemoves(t *testing.T) {
	c := &DummyContainerMinimal{}
	utils.CleanupContainer(c)
	if !c.StopCalled {
		t.Error("Expected Stop to be called")
	}
	if !c.RemoveCalled {
		t.Error("Expected Remove to be called")
	}
}