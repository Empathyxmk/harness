package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestPublicBabelWithAppFactory(t *testing.T) {
	createApp := func(cfg map[string]interface{}) *TestApp {
		app := &TestApp{}
		app.Config = cfg
		flaskbabel.NewBabel().InitApp(app)
		return app
	}
	app := createApp(map[string]interface{}{"BABEL_DEFAULT_LOCALE": "es"})
	withTestRequestContext(app, func() {
		assert.Equal(t, "es", flaskbabel.GetLocale())
	})
}

func TestPublicBabelFactoryDeferredInit(t *testing.T) {
	created := []int{}
	mySelector := func() string {
		created = append(created, 100)
		return "fr"
	}
	b := flaskbabel.NewBabel()
	app := &TestApp{}
	b.InitApp(app, mySelector)
	withTestRequestContext(app, func() {
		assert.Equal(t, "fr", flaskbabel.GetLocale())
		assert.Equal(t, []int{100}, created)
	})
}