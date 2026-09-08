package db

import (
	"testing"
	"time"
)

type DummyDB struct {
	Updated bool
}

type ItemUpdateRunnable struct {
	db      *DummyDB
	running bool
}

func (r *ItemUpdateRunnable) Run() {
	r.running = true
	time.Sleep(10 * time.Millisecond) // Emulate some delayed async update
	if r.db != nil {
		r.db.Updated = true
	}
	r.running = false
}

func (r *ItemUpdateRunnable) IsRunning() bool {
	return r.running
}

func TestItemUpdateRunnable_RunUpdatesDB(t *testing.T) {
	db := &DummyDB{}
	r := &ItemUpdateRunnable{db: db}
	if r.IsRunning() {
		t.Error("Should not be running before start")
	}
	go r.Run()
	time.Sleep(20 * time.Millisecond) // Ensure enough time for Run to finish
	if r.IsRunning() {
		t.Error("Should not be running after run finished")
	}
	if !db.Updated {
		t.Error("DB was not updated by run")
	}
}