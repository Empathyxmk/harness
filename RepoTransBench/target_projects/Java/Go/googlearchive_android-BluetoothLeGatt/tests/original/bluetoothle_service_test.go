package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"bluetoothlegatt/tests"
)

func TestBluetoothLeService_StaticFieldsNotNull(t *testing.T) {
	assert := assert.New(t)
	assert.NotEmpty(tests.BluetoothLeService.ACTION_GATT_CONNECTED, "ACTION_GATT_CONNECTED should not be empty")
	assert.NotEmpty(tests.BluetoothLeService.ACTION_GATT_DISCONNECTED, "ACTION_GATT_DISCONNECTED should not be empty")
	assert.NotEmpty(tests.BluetoothLeService.ACTION_GATT_SERVICES_DISCOVERED, "ACTION_GATT_SERVICES_DISCOVERED should not be empty")
	assert.NotEmpty(tests.BluetoothLeService.ACTION_DATA_AVAILABLE, "ACTION_DATA_AVAILABLE should not be empty")
	assert.NotEmpty(tests.BluetoothLeService.EXTRA_DATA, "EXTRA_DATA should not be empty")
	assert.NotEmpty(tests.BluetoothLeService.UUID_HEART_RATE_MEASUREMENT, "UUID_HEART_RATE_MEASUREMENT should not be empty")
}