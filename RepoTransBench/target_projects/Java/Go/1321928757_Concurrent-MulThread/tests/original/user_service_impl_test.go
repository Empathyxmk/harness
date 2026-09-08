package original

import (
	"sync"
	"testing"
)

// UserDO mimics the Java class for a user entity.
type UserDO struct {
	UserName string
}

// UserReq mimics the Java class for an add-user request.
type UserReq struct {
	UserName string
}

// UserServiceImpl mimics the Java service implementation for users.
type UserServiceImpl struct {
	mu    sync.Mutex
	users []UserDO
}

func NewUserServiceImpl() *UserServiceImpl {
	return &UserServiceImpl{
		users: []UserDO{},
	}
}

func (svc *UserServiceImpl) Add(req UserReq) bool {
	svc.mu.Lock()
	defer svc.mu.Unlock()
	// For this example, always append as in the original `testAddDuplicateUser`
	svc.users = append(svc.users, UserDO{UserName: req.UserName})
	return true
}

func (svc *UserServiceImpl) QueryAll() []UserDO {
	svc.mu.Lock()
	defer svc.mu.Unlock()
	usersCopy := make([]UserDO, len(svc.users))
	copy(usersCopy, svc.users)
	return usersCopy
}

func setupUserService() *UserServiceImpl {
	svc := NewUserServiceImpl()
	// Pre-populate with a user "publicuser"
	svc.Add(UserReq{UserName: "publicuser"})
	return svc
}

func TestAddUser(t *testing.T) {
	userService := setupUserService()
	req := UserReq{UserName: "bob"}
	result := userService.Add(req)
	if !result {
		t.Errorf("Expected true from Add, got false")
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
		t.Errorf("Expected user 'bob' in list, but not found")
	}
}

func TestQueryAll(t *testing.T) {
	userService := setupUserService()
	users := userService.QueryAll()
	if users == nil {
		t.Fatalf("Expected non-nil list of users")
	}
	if len(users) == 0 {
		t.Errorf("Expected at least one user in list (from pre-populate), got 0")
	}
}

func TestAddDuplicateUser(t *testing.T) {
	userService := setupUserService()
	req := UserReq{UserName: "publicuser"}
	result := userService.Add(req)
	if !result {
		t.Errorf("Expected true from Add for duplicate user")
	}
}