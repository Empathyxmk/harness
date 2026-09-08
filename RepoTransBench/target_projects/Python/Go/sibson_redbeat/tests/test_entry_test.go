package tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"redbeat"
)

func createEntry(t *testing.T, name string) *redbeat.RedBeatSchedulerEntry {
	return &redbeat.RedBeatSchedulerEntry{
		Name:    name,
		Task:    "tasks." + name,
		Enabled: true,
		Args:    nil,
		Kwargs:  map[string]interface{}{},
		Options: map[string]interface{}{},
		Schedule: &redbeat.FakeSchedule{
			RunEvery: 42,
		},
	}
}

func TestBasicSave(t *testing.T) {
	e := createEntry(t, "test")
	e.Save()
	assert.Equal(t, "test", e.Name)
}

func TestFromKeyNonexistentKey(t *testing.T) {
	_, err := redbeat.FromKey("doesntexist", &redbeat.App{})
	assert.Error(t, err)
}

func TestFromKeyMissingMeta(t *testing.T) {
	e := createEntry(t, "test")
	e.Save()
	found, err := redbeat.FromKey(e.Name, &redbeat.App{})
	assert.NoError(t, err)
	assert.Equal(t, e.Name, found.Name)
}

func TestNext(t *testing.T) {
	e := createEntry(t, "test")
	e.Save()
	n := e.Next()
	assert.GreaterOrEqual(t, n.LastRunAt.Unix(), e.LastRunAt.Unix())
	assert.Equal(t, e.TotalRunCount+1, n.TotalRunCount)
}

func TestNextOnlyUpdateLastRunAt(t *testing.T) {
	e := createEntry(t, "test")
	e.onlyLastRunAt = true
	n := e.Next()
	assert.True(t, n.LastRunAt.After(e.LastRunAt))
}

func TestDelete(t *testing.T) {
	e := createEntry(t, "test")
	e.Save()
	e.Delete()
}

func TestDueAtNeverRun(t *testing.T) {
	e := createEntry(t, "test")
	got := e.DueAt()
	assert.True(t, got.After(time.Now().Add(-time.Minute)))
}

func TestGenerateKey(t *testing.T) {
	e := createEntry(t, "mock_task_name")
	key := e.GenerateKey(&redbeat.App{}, "mock_task_name")
	assert.Equal(t, "redbeat:mock_task_name", key)
}