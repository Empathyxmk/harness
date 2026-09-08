package original

import (
	"math/rand"
	"sync"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type Callback interface {
	OnGetLock() interface{}
	OnTimeout() interface{}
}

type dummyCallback struct {
	id        int
	logs      *[]string
	sleepTime int
	gotLock   bool
}

func (d *dummyCallback) OnGetLock() interface{} {
	item := "Thread:getLock"
	*d.logs = append(*d.logs, item)
	time.Sleep(time.Duration(d.sleepTime) * time.Millisecond)
	item2 := "Thread:sleeped"
	*d.logs = append(*d.logs, item2)
	d.gotLock = true
	return nil
}
func (d *dummyCallback) OnTimeout() interface{} {
	item := "Thread:timeout"
	*d.logs = append(*d.logs, item)
	d.gotLock = false
	return nil
}

// Simulate ZkDistributedLockTemplate with a simple concurrency sync
type ZkDistributedLockTemplate struct{}

func (z *ZkDistributedLockTemplate) Execute(lockKey string, millis int, cb Callback) {
	gotLock := rand.Intn(2) == 0 // randomly success or fail
	if gotLock {
		cb.OnGetLock()
	} else {
		cb.OnTimeout()
	}
}

func TestTry_ZkReentrantLockTemplate(t *testing.T) {
	template := &ZkDistributedLockTemplate{}
	size := 10 // reduce from 100 for unit test speed
	startWG := sync.WaitGroup{}
	startWG.Add(1)
	endWG := sync.WaitGroup{}
	endWG.Add(size)
	logs := []string{}

	for i := 0; i < size; i++ {
		go func(idx int) {
			defer endWG.Done()
			startWG.Wait()
			sleepTime := rand.Intn(5) * 10
			cb := &dummyCallback{id: idx, logs: &logs, sleepTime: sleepTime}
			template.Execute("test", 5000, cb)
		}(i)
	}
	startWG.Done()
	endWG.Wait()

	// At least all goroutines finished
	assert.Len(t, logs, size)
}

func TestMain_ZkReentrantLockTemplate(t *testing.T) {
	template := &ZkDistributedLockTemplate{}
	cb := &dummyCallback{id: 0, logs: &[]string{}}
	template.Execute("订单流水号", 5000, cb)
	// There should be no panic and gotLock or not is ok
}