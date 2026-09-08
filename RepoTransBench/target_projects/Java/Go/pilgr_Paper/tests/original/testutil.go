package original

import (
	"fmt"
	"reflect"
	"sync"
	"time"
)

// This file provides helpers and stubs for test data/models to mimic the Java environment.

type Person struct {
	Age         int
	Bikes       []string
	PhoneNumbers []PhoneNumber
	Name         string
}

type PersonArg struct {
	Name         string
	Age          int
	Bikes        []string
	PhoneNumbers []PhoneNumber
}

type PhoneNumber struct {
	Number string
}

// genPersonList returns a list of Person objects with generated data.
func GenPersonList(size int) []Person {
	list := make([]Person, size)
	for i := 0; i < size; i++ {
		list[i] = GenPerson(Person{}, i)
	}
	return list
}

// genPersonArgList returns a list of PersonArg objects with generated data.
func GenPersonArgList(size int) []PersonArg {
	list := make([]PersonArg, size)
	for i := 0; i < size; i++ {
		list[i] = GenPersonArg(PersonArg{Name: "name"}, i)
	}
	return list
}

// GenPerson fills a Person or compatible (PersonArg) with sample data for index i.
func GenPerson(p Person, i int) Person {
	p.Age = i
	p.Bikes = make([]string, 2)
	p.Bikes[0] = fmt.Sprintf("Kellys gen#%d", i)
	p.Bikes[1] = fmt.Sprintf("Trek gen#%d", i)
	p.PhoneNumbers = []PhoneNumber{
		{Number: fmt.Sprintf("0-KEEP-CALM%d", i)},
		{Number: fmt.Sprintf("0-USE-PAPER%d", i)},
	}
	return p
}

func GenPersonArg(p PersonArg, i int) PersonArg {
	p.Age = i
	p.Bikes = make([]string, 2)
	p.Bikes[0] = fmt.Sprintf("Kellys gen#%d", i)
	p.Bikes[1] = fmt.Sprintf("Trek gen#%d", i)
	p.PhoneNumbers = []PhoneNumber{
		{Number: fmt.Sprintf("0-KEEP-CALM%d", i)},
		{Number: fmt.Sprintf("0-USE-PAPER%d", i)},
	}
	return p
}

func GenPersonMap(size int) map[int]Person {
	result := make(map[int]Person)
	persons := GenPersonList(size)
	for i, person := range persons {
		result[i] = person
	}
	return result
}

// Dummy implementation of a file-based key-value store, mocking Paper.book functionality
type PaperStore struct {
	mu    sync.RWMutex
	store map[string]interface{}
}

func NewPaperStore() *PaperStore {
	return &PaperStore{store: make(map[string]interface{})}
}

func (ps *PaperStore) Destroy() {
	ps.mu.Lock()
	defer ps.mu.Unlock()
	ps.store = make(map[string]interface{})
}

func (ps *PaperStore) Write(key string, val interface{}) error {
	if key == "" {
		return fmt.Errorf("invalid key")
	}
	if val == nil {
		return fmt.Errorf("value cannot be nil")
	}
	ps.mu.Lock()
	defer ps.mu.Unlock()
	ps.store[key] = val
	return nil
}

func (ps *PaperStore) Read(key string, def ...interface{}) interface{} {
	ps.mu.RLock()
	defer ps.mu.RUnlock()
	if v, ok := ps.store[key]; ok {
		return v
	}
	if len(def) > 0 {
		return def[0]
	}
	return nil
}

func (ps *PaperStore) Contains(key string) bool {
	ps.mu.RLock()
	defer ps.mu.RUnlock()
	_, found := ps.store[key]
	return found
}

func (ps *PaperStore) Delete(key string) {
	ps.mu.Lock()
	defer ps.mu.Unlock()
	delete(ps.store, key)
}

// Simulate lastModified for Paper
type KeyTimestamp struct {
	val      interface{}
	modTime  time.Time
}
type PaperTimestampsStore struct {
	mu    sync.RWMutex
	store map[string]KeyTimestamp
}

func NewPaperTimestampsStore() *PaperTimestampsStore {
	return &PaperTimestampsStore{store: map[string]KeyTimestamp{}}
}

func (p *PaperTimestampsStore) Write(key string, val interface{}) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.store[key] = KeyTimestamp{val, time.Now()}
}

func (p *PaperTimestampsStore) LastModified(key string) int64 {
	p.mu.RLock()
	defer p.mu.RUnlock()
	if item, ok := p.store[key]; ok {
		return item.modTime.UnixNano() / 1e6
	}
	return -1
}

// Helper function for comparisons in compatibility/reflection cases
func DeepEqual(a, b interface{}) bool {
	return reflect.DeepEqual(a, b)
}