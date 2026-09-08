package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Device struct {
	DeviceName string
	DeviceType string
	MacAddress string
}

func NewDevice(name, typ string) *Device {
	return &Device{DeviceName: name, DeviceType: typ}
}

func (d *Device) SetMacAddress(mac string) {
	d.MacAddress = mac
}

func TestDeviceNamePublic(t *testing.T) {
	device := NewDevice("public_device_alpha", "public_type_beta")
	device.SetMacAddress("AA:BB:CC:DD:EE:FF")
	assert.Equal(t, "public_device_alpha", device.DeviceName)
}

func TestDeviceTypePublic(t *testing.T) {
	device := NewDevice("public_device_alpha", "public_type_beta")
	device.SetMacAddress("AA:BB:CC:DD:EE:FF")
	assert.Equal(t, "public_type_beta", device.DeviceType)
}

func TestMacAddressPublic(t *testing.T) {
	device := NewDevice("public_device_alpha", "public_type_beta")
	device.SetMacAddress("AA:BB:CC:DD:EE:FF")
	assert.Equal(t, "AA:BB:CC:DD:EE:FF", device.MacAddress)
}