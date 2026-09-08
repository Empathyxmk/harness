package public_tests

import (
	"math"
	"testing"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestPublicRateLimitExceptionFields(t *testing.T) {
	e := ratelimit.NewRateLimitException("limit reached", 1.25)
	if e.Error() != "limit reached" {
		t.Errorf("Error() wrong, got %v", e.Error())
	}
	if math.Abs(e.PeriodRemaining-1.25) > 1e-9 {
		t.Errorf("period_remaining wrong, got %v", e.PeriodRemaining)
	}
}