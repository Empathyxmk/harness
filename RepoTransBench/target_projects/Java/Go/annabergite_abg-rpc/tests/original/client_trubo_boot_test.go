package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type User struct {
	Name string
}
type UserService interface {
	ExistUser(str string) bool
	GetUser(id int) User
	CreateUser(user User) bool
	ListUser(page int) []User
}
type mockUserService struct{}
func (mockUserService) ExistUser(str string) bool     { return str != "" }
func (mockUserService) GetUser(id int) User           { return User{Name: "user"} }
func (mockUserService) CreateUser(user User) bool     { return user.Name != "" }
func (mockUserService) ListUser(page int) []User      { return []User{{Name: "a"}, {Name: "b"}} }

func TestTruboClientBoot(t *testing.T) {
	var userService UserService = &mockUserService{}
	assert.True(t, userService.ExistUser("foo"))
	user := userService.GetUser(1)
	assert.Equal(t, "user", user.Name)
	assert.True(t, userService.CreateUser(user))
	users := userService.ListUser(1)
	assert.Equal(t, 2, len(users))
}