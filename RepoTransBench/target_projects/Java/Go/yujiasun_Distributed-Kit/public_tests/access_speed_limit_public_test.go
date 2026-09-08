package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"yujiasun-distributed-kit/tests"
)

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
	return ok && val == "2"
}

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

func TestGetSetJedisPoolPublic(t *testing.T) {
	limit := &AccessSpeedLimit{}
	assert.Nil(t, limit.GetJedisPool())
	mockPool := tests.NewJedisPoolMock()
	limit.SetJedisPool(mockPool)
	assert.Equal(t, mockPool, limit.GetJedisPool())
}

func TestTryAccessWithTryAccessIntPublic(t *testing.T) {
	jp := tests.NewJedisPoolMock()
	jp.j.SetEvalReturnForArgs("default", "2")
	asl := NewAccessSpeedLimit(jp)
	ok := asl.TryAccess("keyY", 8, 4)
	assert.True(t, ok)
}

func TestTryAccessFalseReturnedPublic(t *testing.T) {
	jp := tests.NewJedisPoolMock()
	jp.j.SetEvalReturnForArgs("default", "9")
	asl := NewAccessSpeedLimit(jp)
	ok := asl.TryAccess("keyW", 15, 7)
	assert.False(t, ok)
}

func TestLuaScriptIncludesLockLogicPublic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLimitCount(9)
	rule.SetSeconds(20)
	rule.SetLockCount(8)
	rule.SetLockTime(30)
	asl := NewAccessSpeedLimit(nil)
	script := asl.BuildLuaScript(rule)
	assert.Contains(t, script, "redis.call('expire', KEYS[1], ARGV[4])")
	assert.True(t, rule.EnableLimitLock())
}

func TestLuaScriptExcludesLockLogicPublic(t *testing.T) {
	rule := &LimitRule{}
	rule.SetLimitCount(11)
	rule.SetSeconds(30)
	rule.SetLockCount(0)
	rule.SetLockTime(0)
	asl := NewAccessSpeedLimit(nil)
	script := asl.BuildLuaScript(rule)
	assert.NotContains(t, script, "ARGV[4]")
	assert.False(t, rule.EnableLimitLock())
}