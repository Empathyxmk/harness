package public_tests

import (
	"strings"
	"testing"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicInitModuleAllExports(t *testing.T) {
	exported := ratelimit.All
	for _, name := range exported {
		val := ratelimit.Get(name)
		if val == nil {
			t.Errorf("ratelimit.Get(%s) is nil, expected an exported symbol", name)
		}
	}
}

func TestPublicInitLimitsAndRateLimitedAreDecorator(t *testing.T) {
	if ratelimit.Limits.String() != ratelimit.RateLimitDecorator.String() {
		t.Errorf("ratelimit.Limits and RateLimitDecorator should have the same repr")
	}
	if ratelimit.RateLimited.String() != ratelimit.RateLimitDecorator.String() {
		t.Errorf("ratelimit.RateLimited and RateLimitDecorator should have the same repr")
	}
	// Test callability
	if ratelimit.Limits == nil {
		t.Errorf("ratelimit.Limits should be callable/non-nil")
	}
	if ratelimit.RateLimited == nil {
		t.Errorf("ratelimit.RateLimited should be callable/non-nil")
	}
}

func TestPublicVersionStringLength(t *testing.T) {
	v := ratelimit.Version
	if _, ok := interface{}(v).(string); !ok {
		t.Errorf("version should be string, got %T", v)
	}
	if strings.Count(v, ".") < 2 {
		t.Errorf("version string should contain at least 2 dots, got `%v`", v)
	}
}