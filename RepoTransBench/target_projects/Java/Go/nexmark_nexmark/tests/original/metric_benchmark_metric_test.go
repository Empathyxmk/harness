package original

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func formatLongValue(val int) string {
	switch {
	case val >= 1000000:
		return fmt.Sprintf("%.2f M", float64(val)/1e6)
	case val >= 1000:
		return fmt.Sprintf("%.2f K", float64(val)/1e3)
	default:
		return fmt.Sprintf("%d", val)
	}
}

func TestFormatLongValue(t *testing.T) {
	assert.Equal(t, "1.64 M", formatLongValue(1636000))
	assert.Equal(t, "1.60 M", formatLongValue(1600000))
	assert.Equal(t, "232", formatLongValue(232))
	assert.Equal(t, "23.21 K", formatLongValue(23213))
}