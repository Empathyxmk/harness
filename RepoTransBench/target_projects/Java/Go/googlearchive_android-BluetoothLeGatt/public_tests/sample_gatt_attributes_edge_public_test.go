package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"bluetoothlegatt/tests"
)

func TestSampleGattAttributesEdgePublic_LookupNullUuidReturnsAlternateDefault(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("", "alt-default")
	assert.Equal(t, "alt-default", result)
}

func TestSampleGattAttributesEdgePublic_LookupEmptyUuidReturnsAnotherDefault(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("", "no-value")
	assert.Equal(t, "no-value", result)
}

func TestSampleGattAttributesEdgePublic_LookupNullDefaultReturnsNullForAnotherUnknown(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("another-notfound-uuid", nil)
	assert.Equal(t, "", result)
}