package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"bluetoothlegatt/tests"
)

func TestSampleGattAttributes_LookupNullUuidReturnsDefault(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("", "default")
	assert.Equal(t, "default", result)
}

func TestSampleGattAttributes_LookupEmptyUuidReturnsDefault(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("", "empty")
	assert.Equal(t, "empty", result)
}

func TestSampleGattAttributes_LookupNullDefaultReturnsNullForUnknown(t *testing.T) {
	result := tests.SampleGattAttributes.Lookup("notfound-uuid", nil)
	assert.Equal(t, "", result)
}