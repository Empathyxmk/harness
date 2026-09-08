package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type MockUser struct {
	Name string
	Role string
}

type WebApp struct {
}

func (w *WebApp) AccessHome() int {
	return 200
}
func (w *WebApp) AccessMyOrders(authenticated bool) (int, error) {
	if !authenticated {
		return 302, nil // redirect
	}
	return 200, nil
}
func (w *WebApp) AccessAdmin(user MockUser) int {
	if user.Role == "ROLE_ADMIN" {
		return 200
	} else if user.Name == "user1" {
		return 403
	}
	return 403
}

func TestAnyUserCanAccessHome(t *testing.T) {
	app := &WebApp{}
	status := app.AccessHome()
	assert.Equal(t, 200, status)
}

func TestNoAuthUserShouldRedirectLoginWhenPersonalPage(t *testing.T) {
	app := &WebApp{}
	status, _ := app.AccessMyOrders(false)
	assert.Equal(t, 302, status)
}

func TestAuthUserCanAccessPersonalPage(t *testing.T) {
	app := &WebApp{}
	status, _ := app.AccessMyOrders(true)
	assert.Equal(t, 200, status)
}

func TestNotAdminUserCantAccessAdminPage(t *testing.T) {
	app := &WebApp{}
	status := app.AccessAdmin(MockUser{Name: "user1", Role: "ROLE_USER"})
	assert.Equal(t, 403, status)
}