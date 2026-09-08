package public_tests

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

func TestUserMixinIsActivePublic(t *testing.T) {
	user := newUser(100)
	if !user.IsActive() {
		t.Errorf("UserMixin.IsActive should return true")
	}
}

func TestUserMixinIsAuthenticatedPublic(t *testing.T) {
	user := newUser(200)
	if !user.IsAuthenticated() {
		t.Errorf("UserMixin.IsAuthenticated should return true")
	}
}

func TestUserMixinIsAnonymousPublic(t *testing.T) {
	user := newUser(300)
	if user.IsAnonymous() {
		t.Errorf("UserMixin.IsAnonymous should return false")
	}
}

func TestUserMixinGetIDReturnsStrPublic(t *testing.T) {
	user := newUser(456)
	id, _ := user.GetID()
	if id != "456" {
		t.Errorf("GetID integer: expected 456, got %s", id)
	}
	user2 := newUser("xyz")
	id2, _ := user2.GetID()
	if id2 != "xyz" {
		t.Errorf("GetID string: expected 'xyz', got %s", id2)
	}
}

func TestUserMixinGetIDAttributeErrorPublic(t *testing.T) {
	user := newUser(10)
	user.ID = nil
	_, err := user.GetID()
	if err == nil {
		t.Errorf("Expected NotImplementedError")
	}
}

func TestUserMixinEqTruePublic(t *testing.T) {
	user1 := newUser(55)
	user2 := newUser(55)
	if !user1.Equal(user2) {
		t.Errorf("Users with same ID should be equal")
	}
}

func TestUserMixinEqFalsePublic(t *testing.T) {
	user1 := newUser(11)
	user2 := newUser(12)
	if user1.Equal(user2) {
		t.Errorf("Users with different ID should not be equal")
	}
}

func TestUserMixinEqTypePublic(t *testing.T) {
	user := newUser(222)
	if user.Equal(struct{}{}) {
		t.Errorf("User should not be equal to different type")
	}
}

func TestUserMixinHashPublic(t *testing.T) {
	user := newUser(42)
	hash := user.Hash()
	if hash == 0 {
		t.Errorf("Hash should not be zero")
	}
}

func TestAnonymousUserMixinPropertiesPublic(t *testing.T) {
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

func TestAnonymousUserMixinGetIDPublic(t *testing.T) {
	anon := &src.AnonymousUserMixin{}
	if anon.GetID() != nil {
		t.Errorf("AnonymousUser GetID should return nil")
	}
}