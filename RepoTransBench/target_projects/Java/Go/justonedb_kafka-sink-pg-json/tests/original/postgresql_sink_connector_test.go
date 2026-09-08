package original

import (
	"reflect"
	"testing"
)

// --- Mocks / Stubs for the original logic ---

// ConfigDef is a stub for org.apache.kafka.common.config.ConfigDef
type ConfigDef struct {
	Name string
}

// PostgreSQLSinkConnector is a stub implementation with minimal logic.
type PostgreSQLSinkConnector struct {
	startedProps map[string]string
}

func (c *PostgreSQLSinkConnector) Version() string {
	return "1.0"
}

// Start stores the provided properties internally
func (c *PostgreSQLSinkConnector) Start(props map[string]string) {
	c.startedProps = map[string]string{}
	for k, v := range props {
		c.startedProps[k] = v
	}
}

func (c *PostgreSQLSinkConnector) TaskConfigs(maxTasks int) []map[string]string {
	configs := make([]map[string]string, maxTasks)
	for i := range configs {
		// clone startedProps
		propsCopy := map[string]string{}
		for k, v := range c.startedProps {
			propsCopy[k] = v
		}
		configs[i] = propsCopy
	}
	return configs
}

// TaskClass returns an id unique to the type for comparison (simulating the Java .class)
func (c *PostgreSQLSinkConnector) TaskClass() string {
	return "PostgreSQLSinkTask"
}

func (c *PostgreSQLSinkConnector) Stop() {}

func (c *PostgreSQLSinkConnector) Config() *ConfigDef {
	return &ConfigDef{Name: "stub"}
}

// --------------- TESTS ----------------

func TestPostgreSQLSinkConnector_Version(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	got := connector.Version()
	want := "1.0"
	if got != want {
		t.Errorf("Version() = %v; want %v", got, want)
	}
}

func TestPostgreSQLSinkConnector_StartAndTaskConfigs(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	props := map[string]string{"foo": "bar"}
	connector.Start(props)
	configs := connector.TaskConfigs(2)
	if len(configs) != 2 {
		t.Errorf("Expected 2 task configs, got %d", len(configs))
	}
	for _, mp := range configs {
		if mp == nil {
			t.Error("Task config map is nil")
		}
		if v, ok := mp["foo"]; !ok || v != "bar" {
			t.Errorf("Expected foo:bar in task config, got %v", mp)
		}
	}
}

func TestPostgreSQLSinkConnector_TaskClass(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	got := connector.TaskClass()
	want := "PostgreSQLSinkTask"
	if got != want {
		t.Errorf("TaskClass() = %v; want %v", got, want)
	}
}

func TestPostgreSQLSinkConnector_Stop(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	// Just exercise the Stop logic; no state to check
	connector.Stop()
}

func TestPostgreSQLSinkConnector_Config(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	got := connector.Config()
	if got == nil {
		t.Error("Config() returned nil")
	}
}