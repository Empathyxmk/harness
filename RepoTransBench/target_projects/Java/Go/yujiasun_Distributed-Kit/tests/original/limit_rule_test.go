package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// LimitRule is defined in access_speed_limit_unit_test.go to keep test structure clear

func TestGettersAndSetters_LimitRule(t *testing.T) {
	rule := &LimitRule{}
	rule.SetSeconds(15)
	rule.SetLimitCount(10)
	rule.SetLockCount(3)
	rule.SetLockTime(120)

	assert.Equal(t, 15, rule.GetSeconds())
	assert.Equal(t, 10, rule.GetLimitCount())
	assert.Equal(t, 3, rule.GetLockCount())
	assert.Equal(t, 120, rule.GetLockTime())
}

func TestEnableLimitLockFalseWhenZero_LimitRule(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLockTime(0)
	rule.SetLockCount(0)

	assert.False(t, rule.EnableLimitLock())
}

func TestEnableLimitLockFalseWhenOneZero_LimitRule(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLockTime(5)
	rule.SetLockCount(0)

	assert.False(t, rule.EnableLimitLock())

	rule.SetLockTime(0)
	rule.SetLockCount(5)

	assert.False(t, rule.EnableLimitLock())
}

func TestEnableLimitLockTrue_LimitRule(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLockTime(10)
	rule.SetLockCount(3)

	assert.True(t, rule.EnableLimitLock())
}