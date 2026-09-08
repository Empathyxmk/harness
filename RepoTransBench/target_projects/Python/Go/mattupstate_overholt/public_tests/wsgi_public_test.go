package public_tests

import (
	"testing"
	"mattupstate_overholt/wsgi"
)

func TestPublicWSGIApplicationType(t *testing.T) {
	if !wsgi.IsDispatcherMiddleware(wsgi.Application) {
		t.Errorf("wsgi.Application should be an instance of DispatcherMiddleware")
	}
}

func TestPublicWSGIApplicationMapping(t *testing.T) {
	if !wsgi.HasAPIMount(wsgi.Application) {
		t.Error("wsgi.Application should have '/api' in its mounts")
	}
}