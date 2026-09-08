package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ModuleTester struct{}

func (mt ModuleTester) Test() {}

func TestModuleTesterCanRun(t *testing.T) {
	mt := ModuleTester{}
	mt.Test()
	assert.True(t, true)
}