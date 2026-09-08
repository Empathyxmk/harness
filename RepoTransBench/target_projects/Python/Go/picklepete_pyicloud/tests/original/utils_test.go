package tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyKeyring struct {
	Saved   map[string]string
	Deleted []string
}

func NewDummyKeyring() *DummyKeyring {
	return &DummyKeyring{
		Saved:   make(map[string]string),
		Deleted: []string{},
	}
}

func (k *DummyKeyring) GetPassword(system, username string) string {
	return k.Saved[username]
}
func (k *DummyKeyring) SetPassword(system, username, password string) string {
	k.Saved[username] = password
	return "set"
}
func (k *DummyKeyring) DeletePassword(system, username string) string {
	k.Deleted = append(k.Deleted, username)
	return "del"
}

func getPasswordFromKeyring(keyring *DummyKeyring, user string) (string, error) {
	pw := keyring.GetPassword("dummy", user)
	if pw != "" {
		return pw, nil
	}
	return "", errors.New("NoStoredPassword")
}

func passwordExistsInKeyring(keyring *DummyKeyring, user string) bool {
	pw := keyring.GetPassword("dummy", user)
	return pw != ""
}

func storePasswordInKeyring(keyring *DummyKeyring, user, pw string) string {
	return keyring.SetPassword("dummy", user, pw)
}

func deletePasswordInKeyring(keyring *DummyKeyring, user string) string {
	return keyring.DeletePassword("dummy", user)
}

func underscoreToCamelCase(str string, initialCap ...bool) string {
	return UnderscoreToCamelCase(str, initialCap...)
}

func getPassword(keyring *DummyKeyring, user string, interactive bool) (string, error) {
	pw, err := getPasswordFromKeyring(keyring, user)
	if err == nil {
		return pw, nil
	}
	// Simulate non-interactive fail, interactive returns "foo"
	if !interactive {
		return "", errors.New("NoStoredPassword")
	}
	return "foo", nil
}

func TestGetPasswordFromKeyringSuccess(t *testing.T) {
	dkr := NewDummyKeyring()
	dkr.Saved["foo"] = "bar"
	pw, err := getPasswordFromKeyring(dkr, "foo")
	assert.NoError(t, err)
	assert.Equal(t, "bar", pw)
}

func TestGetPasswordFromKeyringFailure(t *testing.T) {
	dkr := NewDummyKeyring()
	_, err := getPasswordFromKeyring(dkr, "not-exist")
	assert.Error(t, err)
}

func TestPasswordExistsInKeyringTrue(t *testing.T) {
	dkr := NewDummyKeyring()
	dkr.Saved["a"] = "b"
	assert.True(t, passwordExistsInKeyring(dkr, "a"))
}

func TestPasswordExistsInKeyringFalse(t *testing.T) {
	dkr := NewDummyKeyring()
	assert.False(t, passwordExistsInKeyring(dkr, "none"))
}

func TestStorePasswordInKeyring(t *testing.T) {
	dkr := NewDummyKeyring()
	out := storePasswordInKeyring(dkr, "x", "y")
	assert.Equal(t, "y", dkr.Saved["x"])
	assert.Equal(t, "set", out)
}

func TestDeletePasswordInKeyring(t *testing.T) {
	dkr := NewDummyKeyring()
	dkr.Saved["delme"] = "foo"
	out := deletePasswordInKeyring(dkr, "delme")
	assert.Contains(t, dkr.Deleted, "delme")
	assert.Equal(t, "del", out)
}

func TestUnderscoreToCamelcaseBasic(t *testing.T) {
	assert.Equal(t, "helloWorld", underscoreToCamelCase("hello_world"))
	assert.Equal(t, "AB", underscoreToCamelCase("A_b", true))
}

func TestGetPasswordInteractiveFalse(t *testing.T) {
	dkr := NewDummyKeyring()
	_, err := getPassword(dkr, "z", false)
	assert.Error(t, err)
}

func TestGetPasswordInteractiveTrue(t *testing.T) {
	dkr := NewDummyKeyring()
	out, err := getPassword(dkr, "z", true)
	assert.NoError(t, err)
	assert.Equal(t, "foo", out)
}