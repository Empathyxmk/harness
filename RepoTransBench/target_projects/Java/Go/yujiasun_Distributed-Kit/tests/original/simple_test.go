package original

import (
	"sync"
	"testing"
	"time"
)

type RedisReentrantLock struct {
	mu *sync.Mutex
}

func NewRedisReentrantLock() *RedisReentrantLock {
	return &RedisReentrantLock{mu: &sync.Mutex{}}
}

func (r *RedisReentrantLock) TryLock(timeout time.Duration) bool {
	r.mu.Lock()
	return true
}

func (r *RedisReentrantLock) Unlock() {
	r.mu.Unlock()
}

func TestMain_SimpleTest(t *testing.T) {
	lock := NewRedisReentrantLock()
	acquired := lock.TryLock(5 * time.Second)
	if acquired {
		// simulate work
		time.Sleep(10 * time.Millisecond)
		lock.Unlock()
	}
}

func Test1_SimpleTest(t *testing.T) {
	template := &struct {
	}{}
	_ = template // Only placeholder as lock template
}