package original

import (
	"testing"
)

type Application struct{}

func GetApplicationInstance() *Application {
	return &Application{}
}

func TestApplicationInstantiation(t *testing.T) {
	app := GetApplicationInstance()
	if app == nil {
		t.Errorf("Expected application instance to be non-nil")
	}
}