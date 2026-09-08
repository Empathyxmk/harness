package original

import (
	"reflect"
	"testing"
)

// Simulated context store for test
type TestContext struct {
	data map[string]interface{}
}

func NewTestContext() *TestContext {
	return &TestContext{data: make(map[string]interface{})}
}

func (ctx *TestContext) Set(key string, value interface{}) {
	ctx.data[key] = value
}

func (ctx *TestContext) GetAll() map[string]interface{} {
	return ctx.data
}

func TestSetContextInMiddlewares(t *testing.T) {
	// Simulate context values set by two middleware
	ctx := NewTestContext()
	ctx.Set("set_context_in_middleware_using_context_method", true)
	ctx.Set("set_context_in_middleware_using_context_object", true)

	expected := map[string]interface{}{
		"set_context_in_middleware_using_context_method": true,
		"set_context_in_middleware_using_context_object": true,
	}
	if !reflect.DeepEqual(ctx.GetAll(), expected) {
		t.Errorf("Expected context: %#v, got: %#v", expected, ctx.GetAll())
	}
}

func TestSetContextInView(t *testing.T) {
	// Simulate context values set by middleware AND view
	ctx := NewTestContext()
	ctx.Set("set_context_in_middleware_using_context_method", true)
	ctx.Set("set_context_in_middleware_using_context_object", true)
	ctx.Set("set_context_in_view", true)

	expected := map[string]interface{}{
		"set_context_in_middleware_using_context_method": true,
		"set_context_in_middleware_using_context_object": true,
		"set_context_in_view": true,
	}
	if !reflect.DeepEqual(ctx.GetAll(), expected) {
		t.Errorf("Expected context: %#v, got: %#v", expected, ctx.GetAll())
	}
}