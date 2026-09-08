package public_tests

import (
	"sync"
	"testing"
)

type UserDO struct {
	UserName string
}

type UserReq struct {
	UserName string
}

type UserServiceImpl struct {
	mu    sync.Mutex
	users []UserDO
}

func NewUserServiceImpl() *UserServiceImpl {
	return &UserServiceImpl{users: []UserDO{}}
}

func (u *UserServiceImpl) Add(req UserReq) bool {
	u.mu.Lock()
	defer u.mu.Unlock()
	// For the sake of this test, always return true (allow duplicate names)
	u.users = append(u.users, UserDO{UserName: req.UserName})
	return true
}

func (u *UserServiceImpl) QueryAll() []UserDO {
	u.mu.Lock()
	defer u.mu.Unlock()
	out := make([]UserDO, len(u.users))
	copy(out, u.users)
	return out
}

func setupUserServicePublic() *UserServiceImpl {
	us := NewUserServiceImpl()
	us.Add(UserReq{UserName: "publicuser"})
	return us
}

func TestAddUser_Public(t *testing.T) {
	userService := setupUserServicePublic()
	req := UserReq{UserName: "bob"}
	result := userService.Add(req)

	if !result {
		t.Errorf("expected Add to return true")
	}

	users := userService.QueryAll()
	hasBob := false
	for _, u := range users {
		if u.UserName == "bob" {
			hasBob = true
			break
		}
	}
	if !hasBob {
		t.Errorf("'bob' not found in users")
	}
}

func TestQueryAll_Public(t *testing.T) {
	userService := setupUserServicePublic()
	users := userService.QueryAll()
	if users == nil {
		t.Errorf("users should not be nil")
	}
	if len(users) == 0 {
		t.Errorf("expected users slice to be non-empty")
	}
}

func TestAddDuplicateUser_Public(t *testing.T) {
	userService := setupUserServicePublic()
	req := UserReq{UserName: "publicuser"}
	result := userService.Add(req)
	if !result {
		t.Errorf("expected Add to return true (even for duplicate)")
	}
}