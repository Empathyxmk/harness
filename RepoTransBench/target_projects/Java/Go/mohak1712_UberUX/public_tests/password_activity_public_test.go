package public_tests

import (
	"testing"
	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestPasswordActivityOnCreateExecutesWithoutCrashPublic(t *testing.T) {
	p := new(tests.PasswordActivity)
	p.On("OnCreate", mock.Anything).Return()
	bundle := tests.Bundle{"public_test_char": "P"}
	p.OnCreate(bundle)
	assert.NotNil(t, p)
}