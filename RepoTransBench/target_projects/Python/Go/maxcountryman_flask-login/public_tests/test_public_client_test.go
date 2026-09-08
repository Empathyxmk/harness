package public_tests

import (
	"testing"

	"github.com/example/flasklogin/src"
)

func TestFlaskLoginClientSetsUserIDPublic(t *testing.T) {
	user := &src.DummyUser{ID: "U987"}
	client := src.NewFlaskLoginClient(user, false)
	if v, ok := client.Session["_user_id"]; !ok || v != "U987" {
		t.Errorf("Expected _user_id to be U987")
	}
	if v, ok := client.Session["_fresh"]; !ok || v != false {
		t.Errorf("Expected _fresh to be false")
	}
}

func TestFlaskLoginClientNoUserPublic(t *testing.T) {
	client := src.NewFlaskLoginClient(nil, false)
	if _, ok := client.Session["_user_id"]; ok {
		t.Errorf("_user_id should not be set")
	}
	if _, ok := client.Session["_fresh"]; ok {
		t.Errorf("_fresh should not be set")
	}
}