package tests

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"redbeat"
)

type RedBeatJSONEncoderTestCase struct{}

func (r *RedBeatJSONEncoderTestCase) dumps(obj interface{}) ([]byte, error) {
	return json.Marshal(obj)
}

func (r *RedBeatJSONEncoderTestCase) loads(data []byte, v interface{}) error {
	return json.Unmarshal(data, v)
}

func TestSchedule(t *testing.T) {
	// Simulate schedule with run_every=3s
	s := &struct {
		RunEvery int `json:"run_every"`
	}{RunEvery: 3}
	data, err := json.Marshal(s)
	assert.NoError(t, err)
	var loaded struct {
		RunEvery int `json:"run_every"`
	}
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, 3, loaded.RunEvery)
}

func TestCrontab(t *testing.T) {
	// Simulate crontab
	c := &struct {
		OrigMinute string `json:"_orig_minute"`
	}{OrigMinute: "0"}
	data, err := json.Marshal(c)
	assert.NoError(t, err)
	var loaded struct {
		OrigMinute string `json:"_orig_minute"`
	}
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, "0", loaded.OrigMinute)
}

func TestDatetime(t *testing.T) {
	d := time.Date(2017, 1, 1, 0, 0, 0, 0, time.UTC)
	data, err := json.Marshal(d)
	assert.NoError(t, err)
	var loaded time.Time
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, 2017, loaded.Year())
}

// The following tests are basic demonstrations as rrule and monkeypatch aren't used in Go

func TestSkipRRule(t *testing.T) {
	// Here, just check that encoding an unsupported type errors
	type DummyType struct{}
	enc := redbeat.RedBeatJSONEncoder{}
	_, err := enc.Marshal(DummyType{})
	assert.Error(t, err)
}

func TestWeekdayEncodeDecode(t *testing.T) {
	// Use int day of week for Go test
	type Weekday struct{ Day int }
	wd := Weekday{Day: 0}
	data, err := json.Marshal(wd)
	assert.NoError(t, err)
	var loaded Weekday
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, 0, loaded.Day)
}

func TestScheduleRelative(t *testing.T) {
	type Sched struct {
		RunEvery int  `json:"run_every"`
		Relative bool `json:"relative"`
	}
	s := Sched{RunEvery: 2, Relative: true}
	data, err := json.Marshal(s)
	assert.NoError(t, err)
	var loaded Sched
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.True(t, loaded.Relative)
	assert.Equal(t, 2, loaded.RunEvery)
}