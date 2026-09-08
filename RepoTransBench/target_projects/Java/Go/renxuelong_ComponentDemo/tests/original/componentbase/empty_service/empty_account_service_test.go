package empty_service

import (
	"testing"
)

// Local interface and empty implementation for test logic
type IAccountService interface {
	IsLogin() bool
	GetAccountId() string
	NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{}
}

type EmptyAccountService struct{}
func (e *EmptyAccountService) IsLogin() bool { return false }
func (e *EmptyAccountService) GetAccountId() string { return "" }
func (e *EmptyAccountService) NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{} {
	return nil
}

func TestIsLoginIsFalse(t *testing.T) {
	var s IAccountService = &EmptyAccountService{}
	if s.IsLogin() {
		t.Errorf("Expected isLogin to be false")
	}
}

func TestGetAccountIdIsNull(t *testing.T) {
	var s IAccountService = &EmptyAccountService{}
	if s.GetAccountId() != "" {
		t.Errorf("Expected GetAccountId to return empty string, got %q", s.GetAccountId())
	}
}

func TestNewUserFragmentIsNull(t *testing.T) {
	var s IAccountService = &EmptyAccountService{}
	if s.NewUserFragment(nil, 0, nil, nil, "") != nil {
		t.Error("Expected NewUserFragment to return nil")
	}
}