package public_tests

import (
	"testing"
)

type DummyEmbeddedPostgres struct {
	started bool
}

func (pg *DummyEmbeddedPostgres) Start(user, pass string) {
	pg.started = (user == "publicUser" && pass == "publicPass")
}

func (pg *DummyEmbeddedPostgres) IsStarted() bool {
	return pg.started
}

func TestCanStartWithDifferentCredentials(t *testing.T) {
	pg := &DummyEmbeddedPostgres{}
	pg.Start("publicUser", "publicPass")
	if !pg.IsStarted() {
		t.Error("Expected IsStarted true for correct credentials")
	}
}

func TestFailsToStartWithWrongCredentials(t *testing.T) {
	pg := &DummyEmbeddedPostgres{}
	pg.Start("bad", "creds")
	if pg.IsStarted() {
		t.Error("Expected IsStarted false for wrong credentials")
	}
}