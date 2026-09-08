package public_tests

import (
	"testing"
)

type InMemoryUserDB struct {
	userData map[string]string
}

type InsecureDataStorage2Activity struct {
	DB *InMemoryUserDB
	User string
	Password string
}

func NewInMemoryUserDBPublic() *InMemoryUserDB {
	return &InMemoryUserDB{userData: make(map[string]string)}
}

func NewInsecureDataStorage2ActivityPublic() *InsecureDataStorage2Activity {
	return &InsecureDataStorage2Activity{
		DB: NewInMemoryUserDBPublic(),
	}
}

func (a *InsecureDataStorage2Activity) SaveCredentials() {
	a.DB.userData[a.User] = a.Password
}

func (a *InsecureDataStorage2Activity) OpenOrCreateDatabase() *InMemoryUserDB {
	return a.DB
}

func TestInsecureDataStorage2Activity_onCreate_createsDBAndTable_public(t *testing.T) {
	act := NewInsecureDataStorage2ActivityPublic()
	db := act.OpenOrCreateDatabase()
	_ = db // Table always exists in mock
}

func TestInsecureDataStorage2Activity_saveCredentials_insertsUserData_public(t *testing.T) {
	a := NewInsecureDataStorage2ActivityPublic()
	a.User = "anotheruser"
	a.Password = "anotherpass"

	a.SaveCredentials()

	db := a.OpenOrCreateDatabase()
	pass, ok := db.userData["anotheruser"]
	if !ok {
		t.Fatalf("User 'anotheruser' not found in DB after public insert")
	}
	if pass != "anotherpass" {
		t.Errorf("Expected password 'anotherpass', got '%s'", pass)
	}
}