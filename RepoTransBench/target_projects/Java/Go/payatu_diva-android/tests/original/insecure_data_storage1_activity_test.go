package original

import (
	"testing"
)

// Simulated shared preferences
type SharedPreferences map[string]string

type InsecureDataStorage1Activity struct {
	Prefs SharedPreferences
	User  string
	Pass  string
}

func NewInsecureDataStorage1Activity() *InsecureDataStorage1Activity {
	return &InsecureDataStorage1Activity{Prefs: make(SharedPreferences)}
}

func (a *InsecureDataStorage1Activity) SaveCredentials() {
	a.Prefs["user"] = a.User
	a.Prefs["password"] = a.Pass
}

func TestInsecureDataStorage1Activity_onCreate_setsLayout(t *testing.T) {
	NewInsecureDataStorage1Activity()
	// No exception/issue expected for layout
}

func TestInsecureDataStorage1Activity_saveCredentials_storesCredentials(t *testing.T) {
	a := NewInsecureDataStorage1Activity()
	a.User = "testuser"
	a.Pass = "secret"

	a.SaveCredentials()

	if got := a.Prefs["user"]; got != "testuser" {
		t.Errorf("Expected user 'testuser', got '%s'", got)
	}
	if got := a.Prefs["password"]; got != "secret" {
		t.Errorf("Expected password 'secret', got '%s'", got)
	}
}