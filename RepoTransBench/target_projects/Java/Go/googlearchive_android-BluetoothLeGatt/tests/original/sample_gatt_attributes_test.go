package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"bluetoothlegatt/tests"
)

func TestSampleGattAttributes_LookupReturnsCorrectNameForKnownService(t *testing.T) {
	uuid := "0000180d-0000-1000-8000-00805f9b34fb"
	expected := "Heart Rate Service"
	actual := tests.SampleGattAttributes.Lookup(uuid, "Default")
	assert.Equal(t, expected, actual)
}

func TestSampleGattAttributes_LookupReturnsCorrectNameForKnownCharacteristic(t *testing.T) {
	uuid := tests.HeartRateMeasurement
	expected := "Heart Rate Measurement"
	actual := tests.SampleGattAttributes.Lookup(uuid, "None")
	assert.Equal(t, expected, actual)
}

func TestSampleGattAttributes_LookupReturnsDefaultForUnknownUuid(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("some-unknown-uuid", "MyDefault")
	assert.Equal(t, "MyDefault", result)
}

func TestSampleGattAttributes_LookupDistinctForManufacturerNameString(t *testing.T) {
	uuid := "00002a29-0000-1000-8000-00805f9b34fb"
	result := tests.SampleGattAttributes.Lookup(uuid, "None")
	assert.Equal(t, "Manufacturer Name String", result)
}

func TestSampleGattAttributes_LookupDeviceInformationService(t *testing.T) {
	uuid := "0000180a-0000-1000-8000-00805f9b34fb"
	expected := "Device Information Service"
	result := tests.SampleGattAttributes.Lookup(uuid, "Unknown")
	assert.Equal(t, expected, result)
}