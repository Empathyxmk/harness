package original

import (
	"testing"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestRateLimitExceptionFields(t *testing.T) {
	e := ratelimit.NewRateLimitException("too many", 3.5)
	if e.Error() != "too many" {
		t.Errorf("Error message mismatch: got %v", e.Error())
	}
	if e.PeriodRemaining != 3.5 {
		t.Errorf("Expected PeriodRemaining=3.5 got %v", e.PeriodRemaining)
	}
}