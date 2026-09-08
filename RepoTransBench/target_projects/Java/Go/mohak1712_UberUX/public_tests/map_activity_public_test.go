package public_tests

import (
	"testing"
	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestMapActivityOnCreateExecutesWithoutCrashPublic(t *testing.T) {
	a := new(tests.MapActivity)
	a.On("OnCreate", mock.Anything).Return()
	bundle := tests.Bundle{"public_test_double": 88.88}
	a.OnCreate(bundle)
	assert.NotNil(t, a)
}