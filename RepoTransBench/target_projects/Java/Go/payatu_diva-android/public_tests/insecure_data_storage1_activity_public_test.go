package public_tests

import (
	"testing"
)

type SharedPreferences map[string]string

type InsecureDataStorage1Activity struct {
	Prefs SharedPreferences
	User  string
	Pass  string
}

func NewInsecureDataStorage1ActivityPublic() *InsecureDataStorage1Activity {
	return &InsecureDataStorage1Activity{Prefs: make(SharedPreferences)}
}

func (a *InsecureDataStorage1Activity) SaveCredentials() {
	a.Prefs["user"] = a.User
	a.Prefs["password"] = a.Pass
}

func TestInsecureDataStorage1Activity_saveCredentials_savesToPrefs_public(t *testing.T) {
	a := NewInsecureDataStorage1ActivityPublic()
	a.User = "publicuser"
	a.Pass = "publicpass"

	a.SaveCredentials()

	if got := a.Prefs["user"]; got != "publicuser" {
		t.Errorf("Expected user 'publicuser', got '%s'", got)
	}
	if got := a.Prefs["password"]; got != "publicpass" {
		t.Errorf("Expected password 'publicpass', got '%s'", got)
	}
}