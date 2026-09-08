package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type LimitRule struct {
	limitCount int
	seconds    int
	lockCount  int
	lockTime   int
}

func (lr *LimitRule) SetSeconds(s int)      { lr.seconds = s }
func (lr *LimitRule) SetLimitCount(l int)   { lr.limitCount = l }
func (lr *LimitRule) SetLockCount(l int)    { lr.lockCount = l }
func (lr *LimitRule) SetLockTime(l int)     { lr.lockTime = l }
func (lr *LimitRule) GetSeconds() int       { return lr.seconds }
func (lr *LimitRule) GetLimitCount() int    { return lr.limitCount }
func (lr *LimitRule) GetLockCount() int     { return lr.lockCount }
func (lr *LimitRule) GetLockTime() int      { return lr.lockTime }
func (lr *LimitRule) EnableLimitLock() bool { return lr.lockTime > 0 && lr.lockCount > 0 }

func TestGettersAndSettersPublic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetSeconds(25)
	rule.SetLimitCount(12)
	rule.SetLockCount(5)
	rule.SetLockTime(200)

	assert.Equal(t, 25, rule.GetSeconds())
	assert.Equal(t, 12, rule.GetLimitCount())
	assert.Equal(t, 5, rule.GetLockCount())
	assert.Equal(t, 200, rule.GetLockTime())
}

func TestEnableLimitLockFalseWhenZeroPublic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLockTime(0)
	rule.SetLockCount(0)

	assert.False(t, rule.EnableLimitLock())
}

func TestEnableLimitLockFalseWhenOneZeroPublic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLockTime(8)
	rule.SetLockCount(0)

	assert.False(t, rule.EnableLimitLock())

	rule.SetLockTime(0)
	rule.SetLockCount(6)

	assert.False(t, rule.EnableLimitLock())
}

func TestEnableLimitLockTruePublic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLockTime(15)
	rule.SetLockCount(4)

	assert.True(t, rule.EnableLimitLock())
}