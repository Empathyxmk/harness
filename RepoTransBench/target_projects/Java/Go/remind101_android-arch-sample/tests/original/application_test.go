package original

import (
	"testing"
)

// No real test logic; it was just Android's ApplicationTest placeholder.
// We'll just test that a struct can be constructed and has expected zero value.
type Application struct {
	Name string
}

func TestApplicationConstruction(t *testing.T) {
	app := Application{Name: "TestApplication"}
	if app.Name != "TestApplication" {
		t.Errorf("Application field was not set properly")
	}
}