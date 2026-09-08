package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ModuleTester struct{}

func (m *ModuleTester) Test() {}

func TestDifferentModuleTesterRuns(t *testing.T) {
	tester := &ModuleTester{}
	tester.Test()
	assert.True(t, true)
}