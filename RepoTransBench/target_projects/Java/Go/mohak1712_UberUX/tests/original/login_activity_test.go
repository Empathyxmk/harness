package original

import (
	"testing"

	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestLoginActivityOnCreateExecutesWithoutCrash(t *testing.T) {
	l := new(tests.LoginActivity)
	l.On("OnCreate", mock.Anything).Return()
	bundle := tests.Bundle{}
	l.OnCreate(bundle)
	assert.NotNil(t, l)
}

func TestLoginActivitySetupWindowAnimationsNoCrash(t *testing.T) {
	l := new(tests.LoginActivity)
	l.On("SetupWindowAnimations").Return()
	l.SetupWindowAnimations()
}