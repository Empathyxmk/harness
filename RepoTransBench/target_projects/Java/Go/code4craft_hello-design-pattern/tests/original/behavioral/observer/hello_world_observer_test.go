package observer

import (
	"testing"
	"bytes"
	"os"

	"github.com/stretchr/testify/assert"
)

// The test sets mock Printer; in Go, use a buffer to capture output.
type HelloWorldObserver struct {
	Printer *bytes.Buffer
}

func NewHelloWorldObserver() *HelloWorldObserver {
	return &HelloWorldObserver{Printer: &bytes.Buffer{}}
}

func (o *HelloWorldObserver) SetPrinter(p *bytes.Buffer) {
	o.Printer = p
}

func (o *HelloWorldObserver) Notify() {
	o.Printer.WriteString("Hello Observer!\n")
}

type Subject struct {
	observers []*HelloWorldObserver
}

func NewSubjectWithObservers() *Subject {
	return &Subject{observers: []*HelloWorldObserver{}}
}

func (s *Subject) Attach(observer *HelloWorldObserver) *Subject {
	s.observers = append(s.observers, observer)
	return s
}

func (s *Subject) NotifyObservers() {
	for _, obs := range s.observers {
		obs.Notify()
	}
}

func TestHelloWorldObserver(t *testing.T) {
	observer := NewHelloWorldObserver()
	buf := &bytes.Buffer{}
	observer.SetPrinter(buf)
	subject := NewSubjectWithObservers().Attach(observer)
	subject.NotifyObservers()
	assert.Equal(t, "Hello Observer!\n", buf.String())
}