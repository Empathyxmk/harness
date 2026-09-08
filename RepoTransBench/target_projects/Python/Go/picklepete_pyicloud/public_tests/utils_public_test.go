package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type PublicDummyKeyring struct {
	Saved   map[string]string
	Deleted []string
}

func NewPublicDummyKeyring() *PublicDummyKeyring {
	return &PublicDummyKeyring{
		Saved:   make(map[string]string),
		Deleted: []string{},
	}
}

func (k *PublicDummyKeyring) GetPassword(system, username string) string {
	return k.Saved[username]
}
func (k *PublicDummyKeyring) SetPassword(system, username, password string) string {
	k.Saved[username] = password
	return "store"
}
func (k *PublicDummyKeyring) DeletePassword(system, username string) string {
	k.Deleted = append(k.Deleted, username)
	return "removed"
}

func getPasswordFromKeyring(keyring *PublicDummyKeyring, user string) (string, error) {
	pw := keyring.GetPassword("dummy", user)
	if pw != "" {
		return pw, nil
	}
	return "", errors.New("NoStoredPassword")
}

func passwordExistsInKeyring(keyring *PublicDummyKeyring, user string) bool {
	pw := keyring.GetPassword("dummy", user)
	return pw != ""
}

func storePasswordInKeyring(keyring *PublicDummyKeyring, user, pw string) string {
	return keyring.SetPassword("dummy", user, pw)
}

func deletePasswordInKeyring(keyring *PublicDummyKeyring, user string) string {
	return keyring.DeletePassword("dummy", user)
}

func underscoreToCamelCase(str string, initialCap ...bool) string {
	words := []rune(str)
	var out []rune
	capitalize := false
	if len(initialCap) > 0 && initialCap[0] {
		capitalize = true
	}
	for i, c := range words {
		if c == '_' {
			capitalize = true
		} else if capitalize {
			if c >= 'a' && c <= 'z' {
				out = append(out, c-32)
			} else {
				out = append(out, c)
			}
			capitalize = false
		} else if i == 0 && !capitalize {
			out = append(out, c)
		} else {
			out = append(out, c)
		}
	}
	return string(out)
}

func getPassword(keyring *PublicDummyKeyring, user string, interactive bool) (string, error) {
	pw, err := getPasswordFromKeyring(keyring, user)
	if err == nil {
		return pw, nil
	}
	if !interactive {
		return "", errors.New("NoStoredPassword")
	}
	return "public_secret", nil
}

func TestGetPasswordFromKeyringSuccess(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	dkr.Saved["baz"] = "qux"
	pw, err := getPasswordFromKeyring(dkr, "baz")
	assert.NoError(t, err)
	assert.Equal(t, "qux", pw)
}

func TestGetPasswordFromKeyringFailure(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	_, err := getPasswordFromKeyring(dkr, "does-not-exist")
	assert.Error(t, err)
}

func TestPasswordExistsInKeyringTrue(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	dkr.Saved["public_user"] = "public_pw"
	assert.True(t, passwordExistsInKeyring(dkr, "public_user"))
}

func TestPasswordExistsInKeyringFalse(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	assert.False(t, passwordExistsInKeyring(dkr, "anonymous"))
}

func TestStorePasswordInKeyring(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	out := storePasswordInKeyring(dkr, "user2", "passwd2")
	assert.Equal(t, "passwd2", dkr.Saved["user2"])
	assert.Equal(t, "store", out)
}

func TestDeletePasswordInKeyring(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	dkr.Saved["deleteme"] = "secret"
	out := deletePasswordInKeyring(dkr, "deleteme")
	assert.Contains(t, dkr.Deleted, "deleteme")
	assert.Equal(t, "removed", out)
}

func TestUnderscoreToCamelcaseBasic(t *testing.T) {
	// Simple underscore to camel case, minimal
	assert.Equal(t, "fooBarBaz", underscoreToCamelCase("foo_bar_baz"))
	assert.Equal(t, "BarC", underscoreToCamelCase("Bar_c", true))
}

func TestGetPasswordInteractiveFalse(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	_, err := getPassword(dkr, "userx", false)
	assert.Error(t, err)
}

func TestGetPasswordInteractiveTrue(t *testing.T) {
	dkr := NewPublicDummyKeyring()
	out, err := getPassword(dkr, "userx", true)
	assert.NoError(t, err)
	assert.Equal(t, "public_secret", out)
}