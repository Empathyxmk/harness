package original

import (
	"testing"
)

type User struct {
	ID   int
	Name string
}

func TestSerializeUser(t *testing.T) {
	u := User{ID: 2, Name: "Alice"}
	if u.ID != 2 || u.Name != "Alice" {
		t.Fatalf("Expected User{2, 'Alice'}, got %+v", u)
	}
}

func TestDeserializeUser(t *testing.T) {
	u := User{ID: 3, Name: "Bob"}
	data := map[string]interface{}{
		"ID":   3,
		"Name": "Bob",
	}
	if u.ID != data["ID"] || u.Name != data["Name"] {
		t.Fatalf("Deserialized user %+v does not match expected %+v", u, data)
	}
}