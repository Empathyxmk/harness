package original

import (
	"testing"

	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestLoginWithPhoneOnCreateExecutesWithoutCrash(t *testing.T) {
	l := new(tests.LoginWithPhone)
	l.On("OnCreate", mock.Anything).Return()
	l.OnCreate(tests.Bundle{})
	assert.NotNil(t, l)
}

func TestLoginWithPhoneSetupWindowAnimationsNoCrash(t *testing.T) {
	l := new(tests.LoginWithPhone)
	l.On("SetupWindowAnimations").Return()
	l.SetupWindowAnimations()
}