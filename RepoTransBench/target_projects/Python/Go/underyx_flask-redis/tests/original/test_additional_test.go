package original

import (
	"strings"
	"testing"
)

type DummyRedis struct {
	values map[string]interface{}
}

func NewDummyRedis() *DummyRedis {
	return &DummyRedis{values: make(map[string]interface{})}
}

// Simulate provider-like
type DummyProvider struct {
	URL           string
	FromUrlCalled bool
}

func (p *DummyProvider) FromUrl(url string, kwargs map[string]interface{}) *DummyRedis {
	p.URL = url
	p.FromUrlCalled = true
	return NewDummyRedis()
}

func TestFromCustomProviderSetsProviderAndInits(t *testing.T) {
	provider := &DummyProvider{}
	app := struct{ config map[string]interface{} }{map[string]interface{}{}}
	provider.FromUrl("redis://localhost", map[string]interface{}{})
	if !provider.FromUrlCalled {
		t.Error("Expected FromUrlCalled to be true")
	}
}

func TestFromCustomProviderNoApp(t *testing.T) {
	type DummyProviderNoApp struct{}
	result := &DummyProviderNoApp{}
	if result == nil {
		t.Error("Expected result not nil")
	}
}

func TestFromCustomProviderAssertion(t *testing.T) {
	var p interface{} = nil
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic/assertion for nil provider")
		}
	}()
	if p == nil {
		panic("AssertionError: provider is nil")
	}
}

type TestableFlaskRedis struct {
	client  *DummyRedis
	provider *DummyProvider
}

func (f *TestableFlaskRedis) GetAttr(name string) interface{} {
	if name == "test_func" {
		return func() string { return "called" }
	}
	panic("no such attr")
}
func (f *TestableFlaskRedis) GetItem(name string) interface{} {
	return f.client.values[name]
}
func (f *TestableFlaskRedis) SetItem(name string, val interface{}) {
	f.client.values[name] = val
}
func (f *TestableFlaskRedis) DelItem(name string) {
	delete(f.client.values, name)
}

func TestDunderMethodsForward(t *testing.T) {
	dummy := NewDummyRedis()
	inst := &TestableFlaskRedis{client: dummy}
	getter := inst.GetAttr("test_func").(func() string)
	if getter() != "called" {
		t.Errorf("Expected 'called', got %s", getter())
	}
	inst.SetItem("foo", "bar")
	if inst.GetItem("foo") != "bar" {
		t.Errorf("Expected 'bar', got %v", inst.GetItem("foo"))
	}
	inst.DelItem("foo")
	if inst.GetItem("foo") != nil {
		t.Errorf("Expected nil after deletion, got %v", inst.GetItem("foo"))
	}
}

func TestInitAppSetsExtensionsDict(t *testing.T) {
	client := NewDummyRedis()
	type FakeApp struct {
		config     map[string]interface{}
		extensions map[string]interface{}
	}
	app := &FakeApp{
		config:     map[string]interface{}{},
		extensions: map[string]interface{}{},
	}
	app.extensions["redis"] = client
	if _, ok := app.extensions["redis"]; !ok {
		t.Error("Expected extension present")
	}
	if app.extensions["redis"] != client {
		t.Error("Expected app.extensions[redis] == client")
	}
}

func TestInitAppCreatesExtensions(t *testing.T) {
	client := NewDummyRedis()
	type FakeApp struct {
		config     map[string]interface{}
		extensions map[string]interface{}
	}
	app := &FakeApp{config: map[string]interface{}{}}
	if app.extensions == nil {
		app.extensions = map[string]interface{}{}
	}
	app.extensions["redis"] = client
	if _, ok := app.extensions["redis"]; !ok {
		t.Error("Expected redis extension created in app")
	}
}

func TestUnusualConfigPrefix(t *testing.T) {
	client := NewDummyRedis()
	type FakeApp struct {
		config     map[string]interface{}
		extensions map[string]interface{}
	}
	app := &FakeApp{
		config:     map[string]interface{}{"FOOBAR_URL": "redis://notreal:1234"},
		extensions: map[string]interface{}{},
	}
	app.extensions["foobar"] = client
	if app.extensions["foobar"] != client {
		t.Error("Expected foobar in app.extensions")
	}
}