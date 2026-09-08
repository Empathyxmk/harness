package empty_service

import (
	"testing"
)

type EmptyAccountService struct{}
func (e *EmptyAccountService) IsLogin() bool { return false }
func (e *EmptyAccountService) GetAccountId() string { return "" }
func (e *EmptyAccountService) NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{} {
	return nil
}

func TestIsLoginDifferent(t *testing.T) {
	s := &EmptyAccountService{}
	if s.IsLogin() {
		t.Errorf("Expected IsLogin to be false")
	}
}

func TestGetAccountIdReturnsEmptyStringPublic(t *testing.T) {
	s := &EmptyAccountService{}
	if s.GetAccountId() != "" {
		t.Errorf("Expected accountId to be empty string, got %q", s.GetAccountId())
	}
}