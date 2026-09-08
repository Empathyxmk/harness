package public_tests

import (
	"testing"
)

type Application struct{}

func GetApplicationInstance() *Application {
	return &Application{}
}

func TestApplicationGetsInstance(t *testing.T) {
	app := GetApplicationInstance()
	if app == nil {
		t.Errorf("Expected application instance to be non-nil")
	}
}