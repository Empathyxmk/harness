package public_tests

import (
	"testing"

	"github.com/spengilley/activityfragmentmvp/tests/original"
)

func TestAppModule_ProvideApplicationDifferentAppInstance(t *testing.T) {
	anotherApp := &original.App{}
	module := &original.AppModule{app: anotherApp}
	returned := module.provideApplication()
	if returned != anotherApp {
		t.Errorf("Expected returned application to be the same as the one passed in")
	}
}