package public_tests

import (
	"reflect"
	"testing"
)

type ConfigDef struct {
	Name string
}

type PostgreSQLSinkConnector struct {
	startedProps map[string]string
}

func (c *PostgreSQLSinkConnector) Version() string {
	return "1.0"
}

func (c *PostgreSQLSinkConnector) Start(props map[string]string) {
	c.startedProps = map[string]string{}
	for k, v := range props {
		c.startedProps[k] = v
	}
}

func (c *PostgreSQLSinkConnector) TaskConfigs(maxTasks int) []map[string]string {
	configs := make([]map[string]string, maxTasks)
	for i := range configs {
		propsCopy := map[string]string{}
		for k, v := range c.startedProps {
			propsCopy[k] = v
		}
		configs[i] = propsCopy
	}
	return configs
}

func (c *PostgreSQLSinkConnector) TaskClass() string {
	return "PostgreSQLSinkTask"
}

func (c *PostgreSQLSinkConnector) Stop() {}

func (c *PostgreSQLSinkConnector) Config() *ConfigDef {
	return &ConfigDef{Name: "public-test"}
}

// ----------------------- TESTS -----------------------

func TestPostgreSQLSinkConnector_VersionPublic(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	got := connector.Version()
	want := "1.0"
	if got != want {
		t.Errorf("Version() = %v; want %v", got, want)
	}
}

func TestPostgreSQLSinkConnector_StartAndTaskConfigsPublic(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	props := map[string]string{
		"host": "localhost",
		"port": "5432",
	}
	connector.Start(props)
	configs := connector.TaskConfigs(3)
	if len(configs) != 3 {
		t.Errorf("Expected 3 task configs, got %d", len(configs))
	}
	for _, mp := range configs {
		if mp == nil {
			t.Error("Task config map is nil")
		}
		if v, ok := mp["host"]; !ok || v != "localhost" {
			t.Errorf("Expected host:localhost in task config, got %v", mp)
		}
		if v, ok := mp["port"]; !ok || v != "5432" {
			t.Errorf("Expected port:5432 in task config, got %v", mp)
		}
	}
}

func TestPostgreSQLSinkConnector_TaskClassPublic(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	got := connector.TaskClass()
	want := "PostgreSQLSinkTask"
	if got != want {
		t.Errorf("TaskClass() = %v; want %v", got, want)
	}
}

func TestPostgreSQLSinkConnector_StopPublic(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	// Exercise Stop
	connector.Stop()
}

func TestPostgreSQLSinkConnector_ConfigPublic(t *testing.T) {
	connector := &PostgreSQLSinkConnector{}
	got := connector.Config()
	if got == nil {
		t.Error("Config() returned nil")
	}
}