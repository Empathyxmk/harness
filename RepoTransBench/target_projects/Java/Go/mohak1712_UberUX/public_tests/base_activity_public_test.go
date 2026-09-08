package public_tests

import (
	"testing"
	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestGetContextPublic(t *testing.T) {
	ba := new(tests.BaseActivity)
	ctx := struct{}{}
	ba.On("GetContext").Return(ctx)
	assert.NotNil(t, ba.GetContext())
}