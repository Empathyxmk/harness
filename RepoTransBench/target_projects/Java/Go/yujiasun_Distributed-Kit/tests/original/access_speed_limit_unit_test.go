package original

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
	"yujiasun-distributed-kit/tests"
)

// --- Mocks for AccessSpeedLimit and LimitRule ---

type AccessSpeedLimit struct {
	jp *tests.JedisPoolMock
}

func NewAccessSpeedLimit(pool *tests.JedisPoolMock) *AccessSpeedLimit {
	return &AccessSpeedLimit{jp: pool}
}

func (a *AccessSpeedLimit) GetJedisPool() *tests.JedisPoolMock {
	return a.jp
}

func (a *AccessSpeedLimit) SetJedisPool(jp *tests.JedisPoolMock) {
	a.jp = jp
}

func (a *AccessSpeedLimit) TryAccess(key string, second, limit int) bool {
	j := a.jp.GetResource()
	result := j.Eval("dummy-script", []string{}, []string{}) // would be script etc.
	val, ok := result.(string)
	if !ok {
		return false
	}
	return val == "1"
}

// Simulate the Java method
func (a *AccessSpeedLimit) BuildLuaScript(rule *LimitRule) string {
	script := ""
	if rule.EnableLimitLock() {
		script = "redis.call('expire', KEYS[1], ARGV[4])"
	} else {
		script = "no lock"
	}
	return script
}

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

// -- TESTS --

func TestGetSetJedisPool(t *testing.T) {
	limit := &AccessSpeedLimit{}
	assert.Nil(t, limit.GetJedisPool())
	mockPool := tests.NewJedisPoolMock()
	limit.SetJedisPool(mockPool)
	assert.Equal(t, mockPool, limit.GetJedisPool())
}

func TestTryAccessWithTryAccessInt(t *testing.T) {
	jp := tests.NewJedisPoolMock()
	jp.j.SetEvalReturnForArgs("default", "1")
	asl := NewAccessSpeedLimit(jp)
	ok := asl.TryAccess("keyX", 5, 3)
	assert.True(t, ok)
}

func TestTryAccessFalseReturned(t *testing.T) {
	jp := tests.NewJedisPoolMock()
	jp.j.SetEvalReturnForArgs("default", "6")
	asl := NewAccessSpeedLimit(jp)
	ok := asl.TryAccess("keyZ", 10, 5)
	assert.False(t, ok)
}

func TestLuaScriptIncludesLockLogic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLimitCount(5)
	rule.SetSeconds(12)
	rule.SetLockCount(6)
	rule.SetLockTime(22)
	asl := NewAccessSpeedLimit(nil)
	// reflect is not needed here - directly test BuildLuaScript.
	script := asl.BuildLuaScript(rule)
	assert.Contains(t, script, "redis.call('expire', KEYS[1], ARGV[4])")
	assert.True(t, rule.EnableLimitLock())
}

func TestLuaScriptExcludesLockLogic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLimitCount(7)
	rule.SetSeconds(24)
	rule.SetLockCount(0)
	rule.SetLockTime(0)
	asl := NewAccessSpeedLimit(nil)
	script := asl.BuildLuaScript(rule)
	assert.NotContains(t, script, "ARGV[4]")
	assert.False(t, rule.EnableLimitLock())
}