package public_tests

import (
	"testing"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicRateLimitExceptionInheritance(t *testing.T) {
	ex := ratelimit.NewRateLimitException("foo", 0.99)
	if _, ok := interface{}(ex).(error); !ok {
		t.Errorf("RateLimitException should implement error")
	}
	if ex.PeriodRemaining != 0.99 {
		t.Errorf("Should have period_remaining=0.99")
	}
}

func TestPublicExceptionStrAndValue(t *testing.T) {
	ex := ratelimit.NewRateLimitException("overload", 2)
	if ex.Error() != "overload" {
		t.Errorf("Error string wrong, got %v", ex.Error())
	}
	if ex.PeriodRemaining != 2 {
		t.Errorf("period_remaining wrong, got %v", ex.PeriodRemaining)
	}
}