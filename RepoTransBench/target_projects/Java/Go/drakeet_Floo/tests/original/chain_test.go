package original

import (
	"testing"
)

// Mocks for interfaces & classes
type TestInterceptor struct {
	called bool
}

func (ti *TestInterceptor) Intercept(chain *Chain) {
	ti.called = true
}

type Chain struct {
	interceptor Interceptor
	callback    func()
}

type Interceptor interface {
	Intercept(chain *Chain)
}

func (c *Chain) SetInterceptor(interceptor Interceptor) {
	c.interceptor = interceptor
}
func (c *Chain) GetInterceptor() Interceptor {
	return c.interceptor
}
func (c *Chain) Proceed() {
	if c.interceptor != nil {
		c.interceptor.Intercept(c)
	}
}
func (c *Chain) SetCallback(cb func()) {
	c.callback = cb
}
func (c *Chain) Callback() {
	if c.callback != nil {
		c.callback()
	}
}

func TestChainSetAndProceed(t *testing.T) {
	chain := &Chain{}
	interceptor := &TestInterceptor{}
	chain.SetInterceptor(interceptor)
	if chain.GetInterceptor() != interceptor {
		t.Error("Interceptor was not set properly")
	}
	chain.Proceed()
	if !interceptor.called {
		t.Error("Interceptor.Intercept should have been called in Proceed")
	}
}

func TestChainCallback(t *testing.T) {
	chain := &Chain{}
	called := false
	chain.SetCallback(func() {
		called = true
	})
	chain.Callback()
	if !called {
		t.Error("Callback was not called")
	}
}

func TestDefaultStates(t *testing.T) {
	chain := &Chain{}
	if chain.GetInterceptor() != nil {
		t.Error("Default interceptor should be nil")
	}
}