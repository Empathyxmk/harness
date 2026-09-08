package original

import (
	"testing"

	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestPasswordActivityOnCreateNoCrash(t *testing.T) {
	p := new(tests.PasswordActivity)
	p.On("OnCreate", mock.Anything).Return()
	bundle := tests.Bundle{}
	p.OnCreate(bundle)
	assert.NotNil(t, p)
}

func TestPasswordActivitySetupWindowAnimations(t *testing.T) {
	p := new(tests.PasswordActivity)
	p.On("SetupWindowAnimations").Return()
	p.SetupWindowAnimations()
}