package original

import (
	"sync"
)

// Counter is a simple model struct used by the tests.
type Counter struct {
	id    int
	value int
	name  string
}

var (
	counterAutoID   = 1000
	counterIDMu     sync.Mutex
)

func newCounter() *Counter {
	counterIDMu.Lock()
	defer counterIDMu.Unlock()
	counterAutoID++
	return &Counter{id: counterAutoID}
}

func (c *Counter) SetValue(val int) {
	c.value = val
}
func (c *Counter) GetValue() int {
	return c.value
}
func (c *Counter) SetId(val int) {
	c.id = val
}
func (c *Counter) GetId() int {
	return c.id
}
func (c *Counter) SetName(name string) {
	c.name = name
}
func (c *Counter) GetName() string {
	return c.name
}

/// A singleton CounterDB for test mocking.
type CounterDatabase struct {
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

func (db *CounterDatabase) SaveCounter(counter *Counter) {
	db.counters[counter.GetId()] = counter
}
func (db *CounterDatabase) GetCounter(id int) *Counter {
	return db.counters[id]
}
func (db *CounterDatabase) GetAllCounters() []*Counter {
	result := []*Counter{}
	for _, c := range db.counters {
		result = append(result, c)
	}
	return result
}
func (db *CounterDatabase) Clear() {
	db.counters = make(map[int]*Counter)
}

// Stubs for PresenterManager, etc.
type PresenterManager struct {
	storage map[string]interface{}
}

var (
	presenterMgrInstance     *PresenterManager
	presenterMgrInstanceOnce sync.Once
)

func GetPresenterManager() *PresenterManager {
	presenterMgrInstanceOnce.Do(func() {
		presenterMgrInstance = &PresenterManager{storage: make(map[string]interface{})}
	})
	return presenterMgrInstance
}

func NewPresenterManager() *PresenterManager {
	return &PresenterManager{storage: make(map[string]interface{})}
}

func (pm *PresenterManager) SavePresenter(key string, presenter interface{}) {
	pm.storage[key] = presenter
}
func (pm *PresenterManager) RestorePresenter(key string) interface{} {
	p, ok := pm.storage[key]
	if ok {
		delete(pm.storage, key)
		return p
	}
	return nil
}