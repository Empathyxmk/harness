package public_tests

import (
	"testing"
	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestLoginWithPhoneOnCreateNoCrashPublic(t *testing.T) {
	l := new(tests.LoginWithPhone)
	l.On("OnCreate", mock.Anything).Return()
	bundle := tests.Bundle{"public_test_number": 42}
	l.OnCreate(bundle)
	assert.NotNil(t, l)
}

func TestLoginWithPhoneSetupWindowAnimationsNoCrashPublic(t *testing.T) {
	l := new(tests.LoginWithPhone)
	l.On("SetupWindowAnimations").Return()
	l.SetupWindowAnimations()
}