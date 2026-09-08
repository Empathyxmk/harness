package public_tests

import (
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
		return nil, &TestError{"Top method failed for container"}
	}
	if c.TopValue != nil {
		return c.TopValue, nil
	}
	val := [][]string{{"1", "2", "3", "4", "5", "6", "7", "gunicorn -w 3 -b :5000 anotherapp:app"}}
	if !c.HasGunicorn {
		val = [][]string{{"z", "y", "x", "w", "v", "u", "t", "python manage.py"}}
	}
	return map[string]interface{}{
		"Processes": val,
	}, nil
}
func (c *DummyContainer) ExecRun(cmd string) ([]byte, error) {
	if c.RaiseOnExecRun {
		return nil, &TestError{"exec_run simulated failure"}
	}
	if c.ExecRunValue != nil {
		return c.ExecRunValue, nil
	}
	return []byte(`{"bar": 43}`), nil
}
func (c *DummyContainer) Logs() ([]byte, error) {
	if c.LogsValue != nil {
		return c.LogsValue, nil
	}
	return []byte("Different logs"), nil
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
type TestError struct{ msg string }
func (e *TestError) Error() string { return e.msg }

func (dc *DummyClient) GetContainer(name string) (*DummyContainer, error) {
	if dc.NotFound {
		return nil, &TestError{"container not present"}
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
		if v == "gunicorn -w 3 -b :5000 anotherapp:app" {
			found = true
		}
	}
	if !found {
		t.Errorf("Expected 'gunicorn -w 3 -b :5000 anotherapp:app' in process names")
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
	top := map[string]interface{}{
		"Processes": [][]string{{"1", "2", "3", "4", "5", "6", "7", "gunicorn -c custom_conf.py anotherapp:app"}},
	}
	c := &DummyContainer{TopValue: top}
	path, err := utils.GetGunicornConfPath(c)
	if err != nil {
		t.Fatalf("GetGunicornConfPath returned error: %v", err)
	}
	if path != "custom_conf.py" {
		t.Errorf("Expected custom_conf.py, got %s", path)
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
	c := &DummyContainer{ExecRunValue: []byte(`{"baz":99}`)}
	cfg, err := utils.GetConfig(c)
	if err != nil {
		t.Fatalf("GetConfig failed: %v", err)
	}
	if v, ok := cfg["baz"]; !ok || v.(float64) != 99 {
		t.Errorf("Expected baz=99, got %v", cfg)
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
	c := &DummyContainer{LogsValue: []byte("xyz789")}
	logs, err := utils.GetLogs(c)
	if err != nil {
		t.Fatalf("GetLogs returned error: %v", err)
	}
	if logs != "xyz789" {
		t.Errorf("Expected logs == 'xyz789', got %q", logs)
	}
}

func TestGetResponseText1(t *testing.T) {
	os.Setenv("PYTHON_VERSION", "3.10")
	msg := utils.GetResponseText1()
	if !strings.Contains(msg, "3.10") {
		t.Errorf("Expected msg to contain '3.10', got %q", msg)
	}
}

type BadContainer struct{}
func (c *BadContainer) Logs() ([]byte, error) {
	return []byte{0xfe}, nil
}
func TestGetLogsUtf8Error(t *testing.T) {
	c := &BadContainer{}
	_, err := utils.GetLogs(c)
	if err == nil || !strings.Contains(err.Error(), "unicode decode error") {
		t.Errorf("Expected unicode decode error, got %v", err)
	}
}