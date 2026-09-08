package original

import (
	"testing"
	"reflect"
)

// --- Mocks / Stubs for the original logic ---

// SinkRecord is a stub for org.apache.kafka.connect.sink.SinkRecord
type SinkRecord struct {
	Topic     string
	Partition int32
	Key       interface{}
	Value     interface{}
	Offset    int64
}

// PostgreSQLSinkTask is a stub implementation with minimal logic.
type PostgreSQLSinkTask struct {
	started bool
	lastPut []SinkRecord
}

// Version returns the connector version as in the Java test.
func (t *PostgreSQLSinkTask) Version() string {
	return "1.0"
}

func (t *PostgreSQLSinkTask) Start(props map[string]string) {
	t.started = true
}

func (t *PostgreSQLSinkTask) Stop() {
	t.started = false
}

// Put simulates putting records.
func (t *PostgreSQLSinkTask) Put(records []SinkRecord) {
	t.lastPut = records
}

// --------------- TESTS ----------------

func TestPostgreSQLSinkTask_Version(t *testing.T) {
	task := &PostgreSQLSinkTask{}
	got := task.Version()
	want := "1.0"
	if got != want {
		t.Errorf("Version() = %v; want %v", got, want)
	}
}

func TestPostgreSQLSinkTask_StartAndStop(t *testing.T) {
	task := &PostgreSQLSinkTask{}
	props := map[string]string{"a": "b"}
	task.Start(props)
	if !task.started {
		t.Error("Start() did not mark task as started")
	}
	task.Stop()
	if task.started {
		t.Error("Stop() did not mark task as stopped")
	}
}

func TestPostgreSQLSinkTask_Put(t *testing.T) {
	task := &PostgreSQLSinkTask{}
	records := []SinkRecord{
		{
			Topic:     "topic",
			Partition: 0,
			Key:       nil,
			Value:     nil,
			Offset:    0,
		},
	}
	task.Put(records)
	if !reflect.DeepEqual(task.lastPut, records) {
		t.Errorf("Put() = %v; want %v", task.lastPut, records)
	}
}