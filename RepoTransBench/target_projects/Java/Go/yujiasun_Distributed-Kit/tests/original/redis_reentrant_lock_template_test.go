package original

import (
	"math/rand"
	"sync"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

// Dummy callback and template similar to zk variant
type Callback interface {
	OnGetLock() interface{}
	OnTimeout() interface{}
}

type dummyCallback struct {
	id        int
	gotLock   bool
	sleepTime int
}

func (d *dummyCallback) OnGetLock() interface{} {
	d.gotLock = true
	time.Sleep(time.Duration(d.sleepTime) * time.Millisecond)
	return nil
}
func (d *dummyCallback) OnTimeout() interface{} {
	d.gotLock = false
	return nil
}

type RedisDistributedLockTemplate struct{}

func (r *RedisDistributedLockTemplate) Execute(lockKey string, millis int, cb Callback) {
	gotLock := rand.Intn(2) == 0
	if gotLock {
		cb.OnGetLock()
	} else {
		cb.OnTimeout()
	}
}

func TestTry_RedisReentrantLockTemplate(t *testing.T) {
	template := &RedisDistributedLockTemplate{}
	size := 10 // reduce from 100 for test
	startWG := sync.WaitGroup{}
	startWG.Add(1)
	endWG := sync.WaitGroup{}
	endWG.Add(size)
	for i := 0; i < size; i++ {
		go func(idx int) {
			defer endWG.Done()
			startWG.Wait()
			cb := &dummyCallback{id: idx, sleepTime: rand.Intn(5) * 10}
			template.Execute("test", 5000, cb)
		}(i)
	}
	startWG.Done()
	endWG.Wait()
}