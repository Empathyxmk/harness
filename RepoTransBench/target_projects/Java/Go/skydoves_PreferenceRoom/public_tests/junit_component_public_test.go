package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type JunitComponent struct {
	DeviceId string
}

func NewJunitComponent(deviceId string) *JunitComponent {
	return &JunitComponent{DeviceId: deviceId}
}

func TestDeviceIdIsSetPublic(t *testing.T) {
	component := NewJunitComponent("public_device_id")
	assert.Equal(t, "public_device_id", component.DeviceId)
}

func TestDeviceIdIsNotDefaultPublic(t *testing.T) {
	component := NewJunitComponent("public_device_id")
	assert.NotEqual(t, "DEFAULT_DEVICE", component.DeviceId)
}