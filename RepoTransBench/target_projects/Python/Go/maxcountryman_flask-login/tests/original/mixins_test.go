package original

import (
	"testing"

	"github.com/example/flasklogin/src"
)

type User struct {
	src.UserMixin
}

func newUser(id interface{}) *User {
	return &User{src.UserMixin{ID: id}}
}

func TestUserMixinIsActive(t *testing.T) {
	user := newUser(1)
	if !user.IsActive() {
		t.Errorf("UserMixin.IsActive should return true")
	}
}

func TestUserMixinIsAuthenticated(t *testing.T) {
	user := newUser(2)
	if !user.IsAuthenticated() {
		t.Errorf("UserMixin.IsAuthenticated should return true")
	}
}

func TestUserMixinIsAnonymous(t *testing.T) {
	user := newUser(3)
	if user.IsAnonymous() {
		t.Errorf("UserMixin.IsAnonymous should return false")
	}
}

func TestUserMixinGetIDReturnsStr(t *testing.T) {
	user := newUser(123)
	id, _ := user.GetID()
	if id != "123" {
		t.Errorf("GetID integer: expected 123, got %s", id)
	}
	user2 := newUser("abc")
	id2, _ := user2.GetID()
	if id2 != "abc" {
		t.Errorf("GetID string: expected 'abc', got %s", id2)
	}
}

func TestUserMixinGetIDAttributeError(t *testing.T) {
	user := newUser(1)
	user.ID = nil
	_, err := user.GetID()
	if err == nil {
		t.Errorf("Expected NotImplementedError")
	}
}

func TestUserMixinEqTrue(t *testing.T) {
	user1 := newUser(9)
	user2 := newUser(9)
	if !user1.Equal(user2) {
		t.Errorf("Users with same ID should be equal")
	}
}

func TestUserMixinEqFalse(t *testing.T) {
	user1 := newUser(1)
	user2 := newUser(2)
	if user1.Equal(user2) {
		t.Errorf("Users with different ID should not be equal")
	}
}

func TestUserMixinEqType(t *testing.T) {
	user := newUser(1)
	if user.Equal(struct{}{}) {
		t.Errorf("User should not be equal to different type")
	}
}

func TestUserMixinHash(t *testing.T) {
	user := newUser(1)
	hash := user.Hash()
	if hash == 0 {
		t.Errorf("Hash should not be zero")
	}
}

func TestAnonymousUserMixinProperties(t *testing.T) {
	anon := &src.AnonymousUserMixin{}
	if anon.IsActive() != false {
		t.Errorf("AnonymousUser IsActive should be false")
	}
	if anon.IsAuthenticated() != false {
		t.Errorf("AnonymousUser IsAuthenticated should be false")
	}
	if anon.IsAnonymous() != true {
		t.Errorf("AnonymousUser IsAnonymous should be true")
	}
}

func TestAnonymousUserMixinGetID(t *testing.T) {
	anon := &src.AnonymousUserMixin{}
	if anon.GetID() != nil {
		t.Errorf("AnonymousUser GetID should return nil")
	}
}