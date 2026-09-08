package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"bluetoothlegatt/tests"
)

func TestDeviceControlActivity_ExtrasConstantsAreNotNull(t *testing.T) {
	assert := assert.New(t)
	assert.NotEmpty(tests.DeviceControlActivity.EXTRAS_DEVICE_NAME, "EXTRAS_DEVICE_NAME should not be empty")
	assert.NotEmpty(tests.DeviceControlActivity.EXTRAS_DEVICE_ADDRESS, "EXTRAS_DEVICE_ADDRESS should not be empty")
}