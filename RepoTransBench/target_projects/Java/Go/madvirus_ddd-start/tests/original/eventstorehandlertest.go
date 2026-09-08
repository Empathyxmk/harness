package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Store struct {
	events []string
}

func (s *Store) Save(event string) {
	s.events = append(s.events, event)
}

type StoreHandler struct {
	store *Store
}

func (h *StoreHandler) HandleEvent(e string) {
	h.store.Save(e)
}

func TestEventStoreHandlerSavesEvents(t *testing.T) {
	store := &Store{}
	handler := &StoreHandler{store: store}
	handler.HandleEvent("EventX")
	handler.HandleEvent("EventY")
	assert.Equal(t, []string{"EventX", "EventY"}, store.events)
}