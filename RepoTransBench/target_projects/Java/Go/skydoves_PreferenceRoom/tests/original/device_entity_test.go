package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type UserDevice struct {
	Version     string
	Uuid        string
	Preferences map[string]interface{}
}

func NewUserDevice() *UserDevice {
	return &UserDevice{Preferences: make(map[string]interface{})}
}
func (u *UserDevice) getEntityName() string {
	return "UserDevice"
}
func (u *UserDevice) versionKeyName() string { return "version" }
func (u *UserDevice) getVersion() string {
	if val, ok := u.Preferences["version"]; ok {
		return val.(string)
	}
	return u.Version
}
func (u *UserDevice) putVersion(v string) { u.Preferences["version"] = v }
func (u *UserDevice) getUuid() string {
	// Simulate decrypt
	if val, ok := u.Preferences["uuid"]; ok {
		return val.(string)
	}
	return u.Uuid
}
func (u *UserDevice) putUuid(uuid string) {
	u.Preferences["uuid"] = uuid // simulate encrypted
}
func (u *UserDevice) uuidKeyName() string { return "uuid" }

func TestVersion(t *testing.T) {
	device := NewUserDevice()
	device.putVersion("1.0.0.0")
	assert.Equal(t, "1.0.0.0", device.getVersion())
}

func TestSecurity(t *testing.T) {
	device := NewUserDevice()
	device.putUuid("00001234-0000-0000-0000-000123456789") // simulate encrypt
	assert.Equal(t, "00001234-0000-0000-0000-000123456789", device.getUuid()) // simulate decrypt
}