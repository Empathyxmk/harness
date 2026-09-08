package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"bluetoothlegatt/tests"
)

func TestSampleGattAttributesPublic_LookupReturnsCorrectNameForAnotherKnownService(t *testing.T) {
	uuid := "0000180a-0000-1000-8000-00805f9b34fb"
	expected := "Device Information Service"
	actual := tests.SampleGattAttributes.Lookup(uuid, "DefaultValue")
	assert.Equal(t, expected, actual)
}

func TestSampleGattAttributesPublic_LookupReturnsCorrectNameForAnotherKnownCharacteristic(t *testing.T) {
	uuid := "00002a29-0000-1000-8000-00805f9b34fb"
	expected := "Manufacturer Name String"
	actual := tests.SampleGattAttributes.Lookup(uuid, "OtherDefault")
	assert.Equal(t, expected, actual)
}

func TestSampleGattAttributesPublic_LookupReturnsDefaultForDifferentUnknownUuid(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("unknown-public-uuid", "OtherDefaultValue")
	assert.Equal(t, "OtherDefaultValue", result)
}

func TestSampleGattAttributesPublic_LookupDistinctForHeartRateMeasurement(t *testing.T) {
	uuid := tests.HeartRateMeasurement
	result := tests.SampleGattAttributes.Lookup(uuid, "UnknownValue")
	assert.Equal(t, "Heart Rate Measurement", result)
}

func TestSampleGattAttributesPublic_LookupHeartRateService(t *testing.T) {
	uuid := "0000180d-0000-1000-8000-00805f9b34fb"
	expected := "Heart Rate Service"
	actual := tests.SampleGattAttributes.Lookup(uuid, "NewUnknown")
	assert.Equal(t, expected, actual)
}