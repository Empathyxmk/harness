package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type MultiLockManager struct {
	locked map[string]string // id -> user
}

func (lm *MultiLockManager) Lock(id string, user string) bool {
	if _, exists := lm.locked[id]; exists {
		return false
	}
	lm.locked[id] = user
	return true
}

func (lm *MultiLockManager) Unlock(id string) {
	delete(lm.locked, id)
}

func TestMultiUserLockManager(t *testing.T) {
	lm := &MultiLockManager{locked: make(map[string]string)}
	ok := lm.Lock("resA", "user1")
	assert.True(t, ok)
	ok = lm.Lock("resA", "user2")
	assert.False(t, ok)
	lm.Unlock("resA")
	ok = lm.Lock("resA", "user2")
	assert.True(t, ok)
}