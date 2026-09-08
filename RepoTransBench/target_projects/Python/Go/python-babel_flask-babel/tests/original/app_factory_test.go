package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

type testAppFactoryFlaskApp struct {
	Config map[string]interface{}
}

func newTestAppFactoryFlaskApp() *testAppFactoryFlaskApp {
	return &testAppFactoryFlaskApp{
		Config: make(map[string]interface{}),
	}
}

func TestAppFactory(t *testing.T) {
	b := flaskbabel.NewBabel()

	localeSelector := func() string {
		return "de_DE"
	}

	createApp := func() *testAppFactoryFlaskApp {
		app := newTestAppFactoryFlaskApp()
		b.InitApp(app, "en_US", localeSelector)
		return app
	}

	app := createApp()
	withTestRequestContext(app, func() {
		assert.Equal(t, "de_DE", flaskbabel.GetLocale())
		assert.Equal(t, "Hallo Peter!", flaskbabel.Gettext("Hello %(name)s!", "Peter"))
	})
}