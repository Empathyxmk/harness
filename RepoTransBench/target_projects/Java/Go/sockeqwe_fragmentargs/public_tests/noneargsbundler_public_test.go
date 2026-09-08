package public_tests

import (
	"testing"
)

func TestPublicTestInstanceSingleton(t *testing.T) {
	a := NoneArgsBundlerGet()
	b := NoneArgsBundlerGet()
	if a != b {
		t.Errorf("get() should be same instance")
	}
}

func TestPublicTestPutNullAlways(t *testing.T) {
	got := NoneArgsBundlerGet().Put("publicKey", "hello", map[string]interface{}{})
	if got != nil {
		t.Errorf("Should always return nil from put")
	}
}

func TestPublicTestGetNullAlways(t *testing.T) {
	got := NoneArgsBundlerGet().Get("anotherKey", map[string]interface{}{})
	if got != nil {
		t.Errorf("Should always return nil from get")
	}
}