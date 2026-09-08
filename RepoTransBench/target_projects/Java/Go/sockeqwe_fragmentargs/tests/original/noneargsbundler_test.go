package original

import (
	"testing"
)

type NoneArgsBundler struct{}

var noneArgsBundlerSingleton = &NoneArgsBundler{}

func NoneArgsBundlerGet() *NoneArgsBundler {
	return noneArgsBundlerSingleton
}

func (*NoneArgsBundler) Put(key string, value interface{}, bundle map[string]interface{}) interface{} {
	return nil
}

func (*NoneArgsBundler) Get(key string, bundle map[string]interface{}) interface{} {
	return nil
}

func TestGetInstanceReturnsSingleton(t *testing.T) {
	a := NoneArgsBundlerGet()
	b := NoneArgsBundlerGet()
	if a != b {
		t.Errorf("get() should always return same instance")
	}
}

func TestPutReturnsNull(t *testing.T) {
	got := NoneArgsBundlerGet().Put("key", 123, map[string]interface{}{})
	if got != nil {
		t.Errorf("put should always return nil, got %v", got)
	}
}

func TestGetReturnsNull(t *testing.T) {
	got := NoneArgsBundlerGet().Get("key", map[string]interface{}{})
	if got != nil {
		t.Errorf("get should always return nil, got %v", got)
	}
}