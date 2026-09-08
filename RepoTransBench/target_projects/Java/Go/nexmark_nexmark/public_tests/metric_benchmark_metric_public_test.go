package public_tests

import (
	"testing"
	"fmt"
	"github.com/stretchr/testify/assert"
)

func formatDoubleValue(val float64) string {
	return fmt.Sprintf("%.4f", val)
}

func formatLongValuePerSecond(val int64, sec float64) string {
	if sec == 0 {
		return "N/A"
	}
	res := fmt.Sprintf("%.2f/s", float64(val)/sec)
	return res
}

func TestFormatDoubleValuePublic(t *testing.T) {
	value := 98765.4321
	formatted := formatDoubleValue(value)
	assert.Equal(t, "98765.4321", formatted)
}

func TestFormatLongValuePerSecondPublic(t *testing.T) {
	value := int64(543210)
	seconds := 36.0
	formatted := formatLongValuePerSecond(value, seconds)
	assert.Contains(t, formatted, "/s")
	assert.NotContains(t, formatted, "N/A")
}