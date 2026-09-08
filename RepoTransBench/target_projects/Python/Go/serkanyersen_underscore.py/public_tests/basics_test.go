package public_tests

import (
	"testing"
	"underscore"
)

func TestIdentityPublic(t *testing.T) {
	if v := underscore.Identity("underscore"); v != "underscore" {
		t.Errorf("expected \"underscore\", got %v", v)
	}
}