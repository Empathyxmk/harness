package public_tests

import (
	"testing"
	"time"
	"github.com/stretchr/testify/assert"
)

func TestTimeProviderPublic_EpochTime(t *testing.T) {
	tp := TimeProvider{}
	timeVal := tp.GetCurrentTimeMillis()
	assert.True(t, timeVal >= 0, "Should retrieve a non-negative time")
}

func TestTimeProviderPublic_TimeHasAdvanced(t *testing.T) {
	tp := TimeProvider{}
	before := tp.GetCurrentTimeMillis()
	time.Sleep(7 * time.Millisecond)
	after := tp.GetCurrentTimeMillis()
	assert.True(t, after > before, "Current time should advance")
}