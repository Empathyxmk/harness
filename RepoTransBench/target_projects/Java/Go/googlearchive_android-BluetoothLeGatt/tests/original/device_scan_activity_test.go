package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"bluetoothlegatt/tests"
)

func TestDeviceScanActivity_ScanPeriodIs10000(t *testing.T) {
	got := tests.DeviceScanActivity.SCAN_PERIOD
	assert.Equal(t, int64(10000), got, "SCAN_PERIOD should be 10000")
}