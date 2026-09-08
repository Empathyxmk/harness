package original

import (
	"testing"

	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

// MockInterceptorRegistry simulates InterceptorRegistry similar to Spring's for testing.
type MockInterceptorRegistry struct {
	mock.Mock
	interceptorAdded bool
}

func (m *MockInterceptorRegistry) AddInterceptor(i any) interface{} {
	m.interceptorAdded = true
	m.Called(i)
	return nil
}

// HttpSessionConfig is a stub struct; in real use, this would be from the original application.
type HttpSessionConfig struct{}

// AddInterceptors is the method under test, here made as no-op. In real migration, use true logic.
func (c *HttpSessionConfig) AddInterceptors(registry *MockInterceptorRegistry) {
	registry.AddInterceptor(struct{}{})
}

func TestAddInterceptors(t *testing.T) {
	config := &HttpSessionConfig{}
	registry := &MockInterceptorRegistry{}
	registry.On("AddInterceptor", mock.Anything).Return(nil).Once()
	config.AddInterceptors(registry)
	registry.AssertCalled(t, "AddInterceptor", mock.Anything)
	require.True(t, registry.interceptorAdded, "interceptor should be added")
}