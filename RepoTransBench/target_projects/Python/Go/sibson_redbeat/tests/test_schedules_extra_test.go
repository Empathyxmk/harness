package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"redbeat"
)

func TestRRuleBasicInit(t *testing.T) {
	sched := redbeat.RRule{Freq: "DAILY", ByHour: 12, ByMinute: 30}
	assert.True(t, sched.Freq == "DAILY")
	assert.Equal(t, 12, sched.ByHour)
	assert.Equal(t, 30, sched.ByMinute)
}

func TestRRuleFieldsAndEq(t *testing.T) {
	s1 := redbeat.RRule{Freq: "DAILY", ByHour: 7}
	s2 := redbeat.RRule{Freq: "DAILY", ByHour: 7}
	s3 := redbeat.RRule{Freq: "HOURLY", ByHour: 7}
	assert.True(t, s1.Equal(&s2))
	assert.False(t, s1.Equal(&s3))
}

func TestRRuleRepr(t *testing.T) {
	s := redbeat.RRule{Freq: "DAILY", ByHour: 6}
	r := s.String()
	assert.Contains(t, r, "rrule")
	assert.Contains(t, r, "byhour")
}