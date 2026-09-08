package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"redbeat"
)

func createEntryPublic(t *testing.T, name string) *redbeat.RedBeatSchedulerEntry {
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

func TestBasicSavePublic(t *testing.T) {
	e := createEntryPublic(t, "public_test")
	e.Save()
	assert.Equal(t, "public_test", e.Name)
}

func TestFromKeyNonexistentKeyPublic(t *testing.T) {
	_, err := redbeat.FromKey("doesnotexist_public", &redbeat.App{})
	assert.Error(t, err)
}

func TestFromKeyMissingMetaPublic(t *testing.T) {
	e := createEntryPublic(t, "entry_missing_meta")
	e.Save()
	found, err := redbeat.FromKey(e.Name, &redbeat.App{})
	assert.NoError(t, err)
	assert.Equal(t, e.Name, found.Name)
}

func TestNextPublic(t *testing.T) {
	e := createEntryPublic(t, "public_next")
	e.Save()
	n := e.Next()
	assert.GreaterOrEqual(t, n.LastRunAt.Unix(), e.LastRunAt.Unix())
	assert.Equal(t, e.TotalRunCount+1, n.TotalRunCount)
}

func TestNextOnlyUpdateLastRunAtPublic(t *testing.T) {
	e := createEntryPublic(t, "public_next_only_update")
	e.onlyLastRunAt = true
	n := e.Next()
	assert.True(t, n.LastRunAt.After(e.LastRunAt))
}

func TestDeletePublic(t *testing.T) {
	e := createEntryPublic(t, "public_delete")
	e.Save()
	e.Delete()
}

func TestDueAtNeverRunPublic(t *testing.T) {
	e := createEntryPublic(t, "public_never_run")
	got := e.DueAt()
	assert.True(t, got.After(e.LastRunAt.Add(-42)))
}

func TestGenerateKeyPublic(t *testing.T) {
	e := createEntryPublic(t, "public_generate_key")
	key := e.GenerateKey(&redbeat.App{}, "another_public_name")
	assert.Equal(t, "redbeat:another_public_name", key)
}