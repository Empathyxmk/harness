package public_tests

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"redbeat"
)

type PublicRedBeatJSONEncoderTestCase struct{}

func TestSchedulePublic(t *testing.T) {
	s := &struct {
		RunEvery int `json:"run_every"`
	}{RunEvery: 5}
	data, err := json.Marshal(s)
	assert.NoError(t, err)
	var loaded struct {
		RunEvery int `json:"run_every"`
	}
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, 5, loaded.RunEvery)
}

func TestCrontabPublic(t *testing.T) {
	c := &struct {
		OrigHour string `json:"_orig_hour"`
	}{OrigHour: "3"}
	data, err := json.Marshal(c)
	assert.NoError(t, err)
	var loaded struct {
		OrigHour string `json:"_orig_hour"`
	}
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, "3", loaded.OrigHour)
}

func TestDatetimePublic(t *testing.T) {
	d := time.Date(2020, 6, 15, 0, 0, 0, 0, time.UTC)
	data, err := json.Marshal(d)
	assert.NoError(t, err)
	var loaded time.Time
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, 2020, loaded.Year())
}

func TestSkipRRulePublic(t *testing.T) {
	type DummyType struct{}
	enc := redbeat.RedBeatJSONEncoder{}
	_, err := enc.Marshal(DummyType{})
	assert.Error(t, err)
}

func TestWeekdayEncodeDecodePublic(t *testing.T) {
	type Weekday struct{ Day int }
	wd := Weekday{Day: 2}
	data, err := json.Marshal(wd)
	assert.NoError(t, err)
	var loaded Weekday
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, 2, loaded.Day)
}

func TestScheduleRelativePublic(t *testing.T) {
	type Sched struct {
		RunEvery int  `json:"run_every"`
		Relative bool `json:"relative"`
	}
	s := Sched{RunEvery: 10, Relative: true}
	data, err := json.Marshal(s)
	assert.NoError(t, err)
	var loaded Sched
	err = json.Unmarshal(data, &loaded)
	assert.NoError(t, err)
	assert.True(t, loaded.Relative)
	assert.Equal(t, 10, loaded.RunEvery)
}