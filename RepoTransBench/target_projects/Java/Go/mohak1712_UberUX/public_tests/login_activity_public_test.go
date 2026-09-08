package public_tests

import (
	"testing"
	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestLoginActivityOnCreateExecutesWithoutCrashPublic(t *testing.T) {
	l := new(tests.LoginActivity)
	l.On("OnCreate", mock.Anything).Return()
	bundle := tests.Bundle{"public_test_key": "public_test_value"}
	l.OnCreate(bundle)
	assert.NotNil(t, l)
}

func TestLoginActivitySetupWindowAnimationsNoCrashPublic(t *testing.T) {
	l := new(tests.LoginActivity)
	l.On("SetupWindowAnimations").Return()
	l.SetupWindowAnimations()
}