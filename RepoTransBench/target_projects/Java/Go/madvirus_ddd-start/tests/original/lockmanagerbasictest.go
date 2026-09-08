package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type LockManager struct {
	locked map[string]bool
}

func (lm *LockManager) Lock(id string) bool {
	if lm.locked[id] {
		return false // Already locked
	}
	lm.locked[id] = true
	return true
}
func (lm *LockManager) Unlock(id string) {
	lm.locked[id] = false
}

func TestLockUnlock(t *testing.T) {
	lm := &LockManager{locked: make(map[string]bool)}
	ok := lm.Lock("resource1")
	assert.True(t, ok)
	ok = lm.Lock("resource1")
	assert.False(t, ok)
	lm.Unlock("resource1")
	ok = lm.Lock("resource1")
	assert.True(t, ok)
}