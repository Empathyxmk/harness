package original

import (
	"testing"
)

func (m *AppModule) provideApplication() *App {
	return m.app
}

func TestAppModule_ProvideApplicationReturnsApp(t *testing.T) {
	app := &App{}
	module := &AppModule{app: app}
	returned := module.provideApplication()
	if returned != app {
		t.Errorf("Expected returned app to be %v but got %v", app, returned)
	}
}