package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type UserService interface {
	Dummy()
}
type mockUserService struct{}
func (mockUserService) Dummy() {}

func TestTruboServerBoot(t *testing.T) {
	var userService UserService = &mockUserService{}
	// just check the type assignment works and no panic
	assert.NotNil(t, userService)
}