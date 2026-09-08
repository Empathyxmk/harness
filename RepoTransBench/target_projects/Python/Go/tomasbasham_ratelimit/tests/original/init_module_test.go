package original

import (
	"reflect"
	"strings"
	"testing"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestInitModuleAllExports(t *testing.T) {
	for _, name := range ratelimit.All {
		// All exported symbols must exist in the ratelimit package
		if !ratelimit.Has(name) {
			t.Errorf("ratelimit should export %s, but does not", name)
		}
	}
}

func TestInitLimitsAndRateLimitedAreDecorator(t *testing.T) {
	if !reflect.DeepEqual(ratelimit.Limits, ratelimit.RateLimitDecorator) {
		t.Errorf("ratelimit.Limits and RateLimitDecorator should point to same implementation")
	}
	if !reflect.DeepEqual(ratelimit.RateLimited, ratelimit.RateLimitDecorator) {
		t.Errorf("ratelimit.RateLimited and RateLimitDecorator should point to same implementation")
	}
	// Test callability (function pointer)
	if reflect.ValueOf(ratelimit.Limits).Kind() != reflect.Func {
		t.Errorf("ratelimit.Limits should be a callable function")
	}
	if reflect.ValueOf(ratelimit.RateLimited).Kind() != reflect.Func {
		t.Errorf("ratelimit.RateLimited should be a callable function")
	}
}

func TestVersionStringExists(t *testing.T) {
	v := ratelimit.Version
	if reflect.TypeOf(v).Kind() != reflect.String {
		t.Errorf("ratelimit.Version should be string but got %v", v)
	}
	if !strings.Contains(v, ".") {
		t.Errorf("ratelimit.Version should contain '.'")
	}
}