package public_tests

import (
	"sync"
)

type Counter struct {
	ID    int
	value int
}

var (
	counterAutoID   = 2000
	counterIDMu     sync.Mutex
)

func newCounter() *Counter {
	counterIDMu.Lock()
	defer counterIDMu.Unlock()
	counterAutoID++
	return &Counter{ID: counterAutoID}
}
func (c *Counter) SetValue(val int) { c.value = val }
func (c *Counter) GetValue() int    { return c.value }
func (c *Counter) SetId(val int)    { c.ID = val }
func (c *Counter) GetId() int       { return c.ID }

func (c *Counter) Increment() {
	c.value++
}
func (c *Counter) Decrement() {
	c.value--
}

type CounterDatabase struct {
	sync.RWMutex
	counters map[int]*Counter
}

var (
	counterDBInstance *CounterDatabase
	counterDBMu       sync.Mutex
)

func GetCounterDatabase() *CounterDatabase {
	counterDBMu.Lock()
	defer counterDBMu.Unlock()
	if counterDBInstance == nil {
		counterDBInstance = &CounterDatabase{counters: make(map[int]*Counter)}
	}
	return counterDBInstance
}

func (db *CounterDatabase) SaveCounter(c *Counter) {
	db.Lock()
	defer db.Unlock()
	db.counters[c.GetId()] = c
}
func (db *CounterDatabase) GetCounter(id int) *Counter {
	db.RLock()
	defer db.RUnlock()
	return db.counters[id]
}
func (db *CounterDatabase) GetAllCounters() []*Counter {
	db.RLock()
	defer db.RUnlock()
	var out []*Counter
	for _, c := range db.counters {
		out = append(out, c)
	}
	return out
}
func (db *CounterDatabase) Clear() {
	db.Lock()
	defer db.Unlock()
	db.counters = make(map[int]*Counter)
}

// PresenterManager stub
type PresenterManager struct {
	store map[string]interface{}
}

var (
	presenterManagerInstance *PresenterManager
	pmOnce                  sync.Once
)

func GetPresenterManager() *PresenterManager {
	pmOnce.Do(func() {
		presenterManagerInstance = &PresenterManager{store: make(map[string]interface{})}
	})
	return presenterManagerInstance
}

func NewPresenterManager() *PresenterManager {
	return &PresenterManager{store: make(map[string]interface{})}
}

func (mgr *PresenterManager) SavePresenter(key string, value interface{}) {
	mgr.store[key] = value
}
func (mgr *PresenterManager) RestorePresenter(key string) interface{} {
	v, ok := mgr.store[key]
	if ok {
		delete(mgr.store, key)
		return v
	}
	return nil
}