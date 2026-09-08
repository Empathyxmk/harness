package componentbase

import (
	"sync"
	"testing"
)

type IAccountService interface {
	IsLogin() bool
	GetAccountId() string
	NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{}
}

type ServiceFactory struct {
	accountService IAccountService
}

var (
	sfInstance *ServiceFactory
	sfOnce     sync.Once
)

func GetInstance() *ServiceFactory {
	sfOnce.Do(func() {
		sfInstance = &ServiceFactory{}
	})
	return sfInstance
}

func (sf *ServiceFactory) SetAccountService(s IAccountService) {
	sf.accountService = s
}

func (sf *ServiceFactory) GetAccountService() IAccountService {
	if sf.accountService == nil {
		return &EmptyAccountService{}
	}
	return sf.accountService
}

type EmptyAccountService struct{}
func (e *EmptyAccountService) IsLogin() bool { return false }
func (e *EmptyAccountService) GetAccountId() string { return "" }
func (e *EmptyAccountService) NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{} {
	return nil
}

// For this public test: DifferentMockAccountService implementation
type DifferentMockAccountService struct{}
func (m *DifferentMockAccountService) IsLogin() bool { return false }
func (m *DifferentMockAccountService) GetAccountId() string { return "public_mock_id" }
func (m *DifferentMockAccountService) NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{} {
	return nil
}

func TestServiceFactory_SingletonInstancePublic(t *testing.T) {
	sfInstance = nil
	sfOnce = sync.Once{}
	instance1 := GetInstance()
	instance2 := GetInstance()
	if instance1 != instance2 {
		t.Errorf("Expected singleton instance, got different pointers")
	}
}

func TestServiceFactory_SetAndGetDifferentMockAccountService(t *testing.T) {
	GetInstance().SetAccountService(nil) // reset state

	service := &DifferentMockAccountService{}
	GetInstance().SetAccountService(service)
	result := GetInstance().GetAccountService()
	if result != service {
		t.Errorf("Expected returned interface to be same as set, got different")
	}
}

func TestServiceFactory_GetAccountServiceReturnsEmptyIfNullPublic(t *testing.T) {
	GetInstance().SetAccountService(nil)
	service := GetInstance().GetAccountService()
	if service == nil {
		t.Fatalf("Expected non-nil service")
	}
	_, ok := service.(*EmptyAccountService)
	if !ok {
		t.Errorf("Expected instance of EmptyAccountService, got %#v", service)
	}
}