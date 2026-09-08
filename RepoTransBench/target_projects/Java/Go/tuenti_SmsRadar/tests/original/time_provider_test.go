package original

import (
	"testing"
	"time"
	"github.com/stretchr/testify/assert"
)

func TestTimeProvider_GetDateReturnsNow(t *testing.T) {
	provider := TimeProvider{}
	before := time.Now()
	result := provider.GetDate()
	after := time.Now()
	assert.False(t, result.IsZero())
	assert.True(t, result.After(before.Add(-time.Millisecond)) && result.Before(after.Add(time.Millisecond)))
}