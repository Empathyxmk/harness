package observer

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Observer interface {
	Update()
}

type DummyObserver struct {
	Updated bool
}

func (d *DummyObserver) Update() {
	d.Updated = true
}

type Subject struct {
	observers []Observer
}

func NewSubject() *Subject {
	return &Subject{observers: []Observer{}}
}

func (s *Subject) Attach(obs Observer) *Subject {
	s.observers = append(s.observers, obs)
	return s
}

func (s *Subject) NotifyObservers() {
	for _, obs := range s.observers {
		obs.Update()
	}
}

func TestAttachAndNotify(t *testing.T) {
	subject := NewSubject()
	obs := &DummyObserver{}
	subject.Attach(obs)
	subject.NotifyObservers()
	assert.True(t, obs.Updated, "Observer should have been updated after notify")
}