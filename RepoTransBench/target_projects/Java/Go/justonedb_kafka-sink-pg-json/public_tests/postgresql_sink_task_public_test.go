package public_tests

import (
	"reflect"
	"testing"
)

// --- Mocks / Stubs for the logic (similar to original tests) ---

type SinkRecord struct {
	Topic     string
	Partition int32
	Key       interface{}
	Value     interface{}
	Offset    int64
}

type PostgreSQLSinkTask struct {
	started bool
	lastPut []SinkRecord
}

func (t *PostgreSQLSinkTask) Version() string {
	return "1.0"
}

func (t *PostgreSQLSinkTask) Start(props map[string]string) {
	t.started = true
}

func (t *PostgreSQLSinkTask) Stop() {
	t.started = false
}

func (t *PostgreSQLSinkTask) Put(records []SinkRecord) {
	t.lastPut = records
}

// ----------------- TESTS ---------------------

func TestPostgreSQLSinkTask_VersionPublic(t *testing.T) {
	task := &PostgreSQLSinkTask{}
	got := task.Version()
	want := "1.0"
	if got != want {
		t.Errorf("Version() = %v; want %v", got, want)
	}
}

func TestPostgreSQLSinkTask_StartAndStopPublic(t *testing.T) {
	task := &PostgreSQLSinkTask{}
	props := map[string]string{
		"username": "alice",
		"password": "securepass",
	}
	task.Start(props)
	if !task.started {
		t.Error("Start() did not mark task as started")
	}
	task.Stop()
	if task.started {
		t.Error("Stop() did not mark task as stopped")
	}
}

func TestPostgreSQLSinkTask_PutPublic(t *testing.T) {
	task := &PostgreSQLSinkTask{}
	records := []SinkRecord{
		{
			Topic:     "public_topic",
			Partition: 1,
			Key:       nil,
			Value:     nil,
			Offset:    123,
		},
	}
	task.Put(records)
	if !reflect.DeepEqual(task.lastPut, records) {
		t.Errorf("Put() = %v; want %v", task.lastPut, records)
	}
}