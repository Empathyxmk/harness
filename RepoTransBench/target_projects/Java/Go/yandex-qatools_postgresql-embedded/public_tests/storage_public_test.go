package public_tests

import (
	"strings"
	"testing"
)

type Storage struct {
	dbName   string
	username string
	password string
}

func NewStorage(dbName, username, password string) *Storage {
	return &Storage{
		dbName:   dbName,
		username: username,
		password: password,
	}
}

func (s *Storage) DbName() string    { return s.dbName }
func (s *Storage) Username() string  { return s.username }
func (s *Storage) Password() string  { return s.password }

func (s *Storage) Equals(o *Storage) bool {
	return s != nil && o != nil &&
		s.dbName == o.dbName &&
		s.username == o.username &&
		s.password == o.password
}
func (s *Storage) HashCode() int {
	// Very simple hash function
	return len(s.dbName) + len(s.username)*31 + len(s.password)*31
}
func (s *Storage) String() string {
	return "Storage " + s.dbName + " " + s.username + " " + s.password
}

func TestConstructorAndGettersWithDifferentData(t *testing.T) {
	storage := NewStorage("alt-public-db", "strange-user", "weird-password")
	if storage.DbName() != "alt-public-db" {
		t.Errorf("Expected dbName 'alt-public-db', got '%s'", storage.DbName())
	}
	if storage.Username() != "strange-user" {
		t.Errorf("Expected username 'strange-user', got '%s'", storage.Username())
	}
	if storage.Password() != "weird-password" {
		t.Errorf("Expected password 'weird-password', got '%s'", storage.Password())
	}
}

func TestEqualsAndHashCodeWithDifferentData(t *testing.T) {
	s1 := NewStorage("random_public_db_1", "randomUser", "randomPass")
	s2 := NewStorage("random_public_db_1", "randomUser", "randomPass")
	s3 := NewStorage("random_public_db_2", "otherUser", "otherPass")

	if !s1.Equals(s2) {
		t.Error("s1 should equal s2")
	}
	if s1.Equals(s3) {
		t.Error("s1 should NOT equal s3")
	}
	if s1.HashCode() != s2.HashCode() {
		t.Error("Expected hash codes to match for eq storages")
	}
	if s1.HashCode() == s3.HashCode() {
		t.Error("Expected hash codes to differ for diff storages")
	}
}

func TestToStringWithDifferentData(t *testing.T) {
	storage := NewStorage("string_check_db", "toStringUser", "toStringPass")
	out := storage.String()
	if !strings.Contains(out, "string_check_db") ||
		!strings.Contains(out, "toStringUser") ||
		!strings.Contains(out, "toStringPass") {
		t.Errorf("Expected toString output to contain all struct fields, got '%s'", out)
	}
}