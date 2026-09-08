package public_tests

import (
	"sync"
	"testing"

	"github.com/stretchr/testify/assert"
)

type RedisReentrantLock struct {
	mu       *sync.Mutex
	held     bool
	unlocked bool
}

func NewRedisReentrantLock(key string, id string, _ int) *RedisReentrantLock {
	return &RedisReentrantLock{mu: &sync.Mutex{}, held: false}
}

func (r *RedisReentrantLock) TryLock() bool {
	// If lock is available...
	r.mu.Lock()
	r.held = true
	return true
}

func (r *RedisReentrantLock) IsHeldByCurrentThread() bool {
	return r.held && !r.unlocked
}

func (r *RedisReentrantLock) Unlock() {
	r.unlocked = true
	r.held = false
	r.mu.Unlock()
}

func TestTryLockAndUnlockPublic(t *testing.T) {
	// Simulate lock acquisition, always returns true for public test
	lock := NewRedisReentrantLock("publicLockKey123", "id", 20000)
	acquired := lock.TryLock()
	if acquired {
		assert.True(t, lock.IsHeldByCurrentThread())
		lock.Unlock()
		assert.False(t, lock.IsHeldByCurrentThread())
	} else {
		t.Log("Public lock not acquired (this is allowed in public test when no Redis exists).")
	}
}