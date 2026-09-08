package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type OptimisticLock struct {
	version int
}

func (o *OptimisticLock) Update(newVersion int) error {
	if newVersion <= o.version {
		return errors.New("VersionConflict")
	}
	o.version = newVersion
	return nil
}

func TestOptimisticLockNoConflict(t *testing.T) {
	lock := &OptimisticLock{version: 1}
	err := lock.Update(2)
	assert.NoError(t, err)
}

func TestOptimisticLockConflict(t *testing.T) {
	lock := &OptimisticLock{version: 2}
	err := lock.Update(1)
	assert.Error(t, err)
	assert.EqualError(t, err, "VersionConflict")
}