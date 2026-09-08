package original

import (
	"testing"

	"github.com/example/tomasbasham_ratelimit/ratelimit"
)

func TestRateLimitExceptionMessageAndPeriod(t *testing.T) {
	e := ratelimit.NewRateLimitException("limit reached", 4.5)
	if _, ok := interface{}(e).(error); !ok {
		t.Errorf("should be an error")
	}
	if e.PeriodRemaining != 4.5 {
		t.Errorf("expected period_remaining=4.5, got %v", e.PeriodRemaining)
	}
	if e.Error() != "limit reached" {
		t.Errorf("Error string was '%v', expected 'limit reached'", e.Error())
	}
}