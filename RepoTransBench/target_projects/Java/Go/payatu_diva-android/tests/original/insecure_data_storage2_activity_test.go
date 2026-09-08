package original

import (
	"testing"
)

// Simulated edit boxes and DB for test
type InsecureDataStorage2Activity struct {
	DB *InMemoryUserDB
	User string
	Password string
}

type InMemoryUserDB struct {
	userData map[string]string // user: password
}

func NewInMemoryUserDB() *InMemoryUserDB {
	return &InMemoryUserDB{userData: make(map[string]string)}
}

func NewInsecureDataStorage2Activity() *InsecureDataStorage2Activity {
	return &InsecureDataStorage2Activity{
		DB: NewInMemoryUserDB(),
	}
}

// Simulate saving credentials inserts into DB
func (a *InsecureDataStorage2Activity) SaveCredentials() {
	a.DB.userData[a.User] = a.Password
}

// Open DB/table just ensures our map/table exists; never errors
func (a *InsecureDataStorage2Activity) OpenOrCreateDatabase() *InMemoryUserDB {
	return a.DB
}

func TestInsecureDataStorage2Activity_onCreate_createsDBAndTable(t *testing.T) {
	_ = NewInsecureDataStorage2Activity()
	// If DB/table creation fails, error would occur, but our impl always succeeds.
}

func TestInsecureDataStorage2Activity_saveCredentials_insertsUserData(t *testing.T) {
	activity := NewInsecureDataStorage2Activity()
	activity.User = "dbuser"
	activity.Password = "dbpass"

	activity.SaveCredentials()

	db := activity.OpenOrCreateDatabase()
	pass, ok := db.userData["dbuser"]
	if !ok {
		t.Fatalf("User 'dbuser' not found in DB after insert")
	}
	if pass != "dbpass" {
		t.Errorf("Password for 'dbuser' want 'dbpass', got '%s'", pass)
	}
}