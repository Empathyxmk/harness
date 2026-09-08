package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Event struct {
	Name string
}

type Handler interface {
	Handle(Event)
	EventsHandled() []string
}

type TestHandler struct {
	handled []string
}

func (th *TestHandler) Handle(e Event) {
	th.handled = append(th.handled, e.Name)
}

func (th *TestHandler) EventsHandled() []string {
	return th.handled
}

type EventForwarder struct {
	handlers []Handler
}

func (f *EventForwarder) RegisterHandler(h Handler) {
	f.handlers = append(f.handlers, h)
}

func (f *EventForwarder) Forward(e Event) {
	for _, h := range f.handlers {
		h.Handle(e)
	}
}

func TestEventForwarderForwardsToAllHandlers(t *testing.T) {
	fwd := &EventForwarder{}
	h1 := &TestHandler{}
	h2 := &TestHandler{}
	fwd.RegisterHandler(h1)
	fwd.RegisterHandler(h2)
	event := Event{Name: "OrderPlaced"}
	fwd.Forward(event)
	assert.Equal(t, []string{"OrderPlaced"}, h1.EventsHandled())
	assert.Equal(t, []string{"OrderPlaced"}, h2.EventsHandled())
}