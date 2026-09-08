package tests

import (
	"errors"
	"os"
	"strings"
	"testing"

	"github.com/example/tiangolo_meinheld-gunicorn-flask-docker/utils"
)

type DummyContainer struct {
	TopValue        map[string]interface{}
	ExecRunValue    []byte
	LogsValue       []byte
	HasGunicorn     bool
	RaiseOnTop      bool
	RaiseOnExecRun  bool
	StopCalled      bool
	RemoveCalled    bool
}

func (c *DummyContainer) Top() (map[string]interface{}, error) {
	if c.RaiseOnTop {
		return nil, errors.New("Cannot get top of container")
	}
	if c.TopValue != nil {
		return c.TopValue, nil
	}
	val := [][]string{{"a", "b", "c", "d", "e", "f", "g", "gunicorn -c conf.py app:app"}}
	if !c.HasGunicorn {
		val = [][]string{{"a", "b", "c", "d", "e", "f", "g", "python app.py"}}
	}
	return map[string]interface{}{
		"Processes": val,
	}, nil
}
func (c *DummyContainer) ExecRun(cmd string) ([]byte, error) {
	if c.RaiseOnExecRun {
		return nil, errors.New("exec_run failed")
	}
	if c.ExecRunValue != nil {
		return c.ExecRunValue, nil
	}
	return []byte(`{"key": "value"}`), nil
}
func (c *DummyContainer) Logs() ([]byte, error) {
	if c.LogsValue != nil {
		return c.LogsValue, nil
	}
	return []byte("Some logs"), nil
}
func (c *DummyContainer) Stop() {
	c.StopCalled = true
}
func (c *DummyContainer) Remove() {
	c.RemoveCalled = true
}

type DummyClient struct {
	Container  *DummyContainer
	NotFound   bool
}

func (dc *DummyClient) GetContainer(name string) (*DummyContainer, error) {
	if dc.NotFound {
		return nil, errors.New("not found")
	}
	return dc.Container, nil
}

func TestGetProcessNames(t *testing.T) {
	c := &DummyContainer{}
	res, err := utils.GetProcessNames(c)
	if err != nil {
		t.Fatalf("GetProcessNames returned error: %v", err)
	}
	found := false
	for _, v := range res {
		if v == "gunicorn -c conf.py app:app" {
			found = true
		}
	}
	if !found {
		t.Errorf("Expected 'gunicorn -c conf.py app:app' in process names")
	}
}

func TestGetProcessNamesEmpty(t *testing.T) {
	c := &DummyContainer{HasGunicorn: false}
	res, err := utils.GetProcessNames(c)
	if err != nil {
		t.Fatalf("GetProcessNames returned error: %v", err)
	}
	if len(res) != 0 {
		t.Errorf("Expected empty list, got %v", res)
	}
}

func TestGetGunicornConfPath(t *testing.T) {
	c := &DummyContainer{}
	path, err := utils.GetGunicornConfPath(c)
	if err != nil {
		t.Fatalf("GetGunicornConfPath returned error: %v", err)
	}
	if path != "conf.py" {
		t.Errorf("Expected conf.py, got %s", path)
	}
}

func TestGetGunicornConfPathNoGunicorn(t *testing.T) {
	c := &DummyContainer{HasGunicorn: false}
	_, err := utils.GetGunicornConfPath(c)
	if err == nil {
		t.Error("Expected error with no gunicorn process, got nil")
	}
}

func TestGetConfig(t *testing.T) {
	c := &DummyContainer{ExecRunValue: []byte(`{"foo":42}`)}
	cfg, err := utils.GetConfig(c)
	if err != nil {
		t.Fatalf("GetConfig failed: %v", err)
	}
	if v, ok := cfg["foo"]; !ok || v.(float64) != 42 {
		t.Errorf("Expected foo=42, got %v", cfg)
	}
}

func TestGetConfigExecRunError(t *testing.T) {
	c := &DummyContainer{RaiseOnExecRun: true}
	_, err := utils.GetConfig(c)
	if err == nil {
		t.Error("Expected error when exec_run fails, got nil")
	}
}

func TestRemovePreviousContainerFound(t *testing.T) {
	c := &DummyContainer{}
	client := &DummyClient{Container: c}
	_ = utils.RemovePreviousContainer(client)
	if !c.StopCalled || !c.RemoveCalled {
		t.Errorf("Expected Stop and Remove to be called")
	}
}

func TestRemovePreviousContainerNotfound(t *testing.T) {
	client := &DummyClient{NotFound: true}
	err := utils.RemovePreviousContainer(client)
	if err != nil {
		t.Errorf("Expected no error when not found, got %v", err)
	}
}

func TestGetLogs(t *testing.T) {
	c := &DummyContainer{LogsValue: []byte("abc123")}
	logs, err := utils.GetLogs(c)
	if err != nil {
		t.Fatalf("GetLogs returned error: %v", err)
	}
	if logs != "abc123" {
		t.Errorf("Expected logs == 'abc123', got %q", logs)
	}
}

// This test uses os.Setenv to simulate monkeypatch.
func TestGetResponseText1(t *testing.T) {
	os.Setenv("PYTHON_VERSION", "3.9")
	msg := utils.GetResponseText1()
	if !strings.Contains(msg, "3.9") {
		t.Errorf("Expected msg to contain '3.9', got %q", msg)
	}
}

// Go's string() returns valid UTF-8; to simulate decode error, we rely on our utf8Valid helper.
type BadContainer struct{}
func (c *BadContainer) Logs() ([]byte, error) {
	return []byte{0xff}, nil
}
func TestGetLogsUtf8Error(t *testing.T) {
	c := &BadContainer{}
	_, err := utils.GetLogs(c)
	if err == nil || !strings.Contains(err.Error(), "unicode decode error") {
		t.Errorf("Expected unicode decode error, got %v", err)
	}
}