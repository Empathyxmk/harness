package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type JdbcEventStore struct {
	storage map[string]string
}

func (s *JdbcEventStore) SaveEvent(id string, payload string) {
	if s.storage == nil {
		s.storage = make(map[string]string)
	}
	s.storage[id] = payload
}
func (s *JdbcEventStore) GetEvent(id string) string {
	return s.storage[id]
}

func TestJdbcEventStoreSaveAndRetrieve(t *testing.T) {
	store := &JdbcEventStore{}
	store.SaveEvent("evt-1", "payload-1")
	got := store.GetEvent("evt-1")
	assert.Equal(t, "payload-1", got)
}