package original

import (
	"testing"

	"github.com/example/flasklogin/src"
)

func TestFlaskLoginClientSetsUserID(t *testing.T) {
	user := &src.DummyUser{ID: "U123"}
	client := src.NewFlaskLoginClient(user, false)
	if v, ok := client.Session["_user_id"]; !ok || v != "U123" {
		t.Errorf("Expected _user_id to be U123")
	}
	if v, ok := client.Session["_fresh"]; !ok || v != false {
		t.Errorf("Expected _fresh to be false")
	}
}

func TestFlaskLoginClientNoUser(t *testing.T) {
	client := src.NewFlaskLoginClient(nil, false)
	if _, ok := client.Session["_user_id"]; ok {
		t.Errorf("_user_id should not be set")
	}
	if _, ok := client.Session["_fresh"]; ok {
		t.Errorf("_fresh should not be set")
	}
}