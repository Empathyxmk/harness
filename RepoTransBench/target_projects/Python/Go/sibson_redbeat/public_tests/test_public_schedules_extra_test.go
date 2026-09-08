package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"redbeat"
)

func TestRRuleBasicInitPublic(t *testing.T) {
	sched := redbeat.RRule{Freq: "WEEKLY", ByHour: 8, ByMinute: 15}
	assert.True(t, sched.Freq == "WEEKLY")
	assert.Equal(t, 8, sched.ByHour)
	assert.Equal(t, 15, sched.ByMinute)
}

func TestRRuleFieldsAndEqPublic(t *testing.T) {
	s1 := redbeat.RRule{Freq: "WEEKLY", ByHour: 8}
	s2 := redbeat.RRule{Freq: "WEEKLY", ByHour: 8}
	s3 := redbeat.RRule{Freq: "MONTHLY", ByHour: 8}
	assert.True(t, s1.Equal(&s2))
	assert.False(t, s1.Equal(&s3))
}

func TestRRuleReprPublic(t *testing.T) {
	s := redbeat.RRule{Freq: "WEEKLY", ByHour: 4}
	r := s.String()
	assert.Contains(t, r, "rrule")
	assert.Contains(t, r, "byhour")
}