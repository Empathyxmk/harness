package componentbase

import (
	"testing"
	"sync"
)

type IAccountService interface {
	IsLogin() bool
	GetAccountId() string
	NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{}
}

// --- Implementation Stubs to enable test translation ---

// ServiceFactory is a singleton for the sake of these tests
type ServiceFactory struct {
	accountService IAccountService
}

var (
	factoryInstance     *ServiceFactory
	factoryOnce         sync.Once
)

// GetInstance returns singleton instance
func GetInstance() *ServiceFactory {
	factoryOnce.Do(func() {
		factoryInstance = &ServiceFactory{}
	})
	return factoryInstance
}

func (f *ServiceFactory) SetAccountService(s IAccountService) {
	f.accountService = s
}

func (f *ServiceFactory) GetAccountService() IAccountService {
	if f.accountService == nil {
		// Return default empty implementation
		return &EmptyAccountService{}
	}
	return f.accountService
}

// --- EmptyAccountService and mock for testing ---

type EmptyAccountService struct {}
func (e *EmptyAccountService) IsLogin() bool { return false }
func (e *EmptyAccountService) GetAccountId() string { return "" }
func (e *EmptyAccountService) NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{} {
	return nil
}

// --- Mocks for testing ---

type MockAccountService struct {}
func (m *MockAccountService) IsLogin() bool { return true }
func (m *MockAccountService) GetAccountId() string { return "mock" }
func (m *MockAccountService) NewUserFragment(a interface{}, containerId int, manager interface{}, bundle interface{}, tag string) interface{} {
	return nil
}

func TestServiceFactory_SingletonInstance(t *testing.T) {
	// Clean state for singletons
	factoryInstance = nil
	factoryOnce = sync.Once{}

	instance1 := GetInstance()
	instance2 := GetInstance()
	if instance1 != instance2 {
		t.Errorf("Expected singleton instance, got different pointers")
	}
}

func TestServiceFactory_SetAndGetAccountService(t *testing.T) {
	GetInstance().SetAccountService(nil) // reset

	mockService := &MockAccountService{}
	GetInstance().SetAccountService(mockService)
	result := GetInstance().GetAccountService()
	if result != mockService {
		t.Errorf("Expected returned interface to be same as set, got different")
	}
}

func TestServiceFactory_GetAccountServiceReturnsEmptyIfNil(t *testing.T) {
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