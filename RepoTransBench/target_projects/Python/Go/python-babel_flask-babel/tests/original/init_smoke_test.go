package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

type DummyApp struct {
	Config     map[string]interface{}
	Extensions map[string]interface{}
}

func newDummyApp() *DummyApp {
	return &DummyApp{
		Config:     map[string]interface{}{},
		Extensions: map[string]interface{}{},
	}
}

func TestBabelInitAndAppProperties(t *testing.T) {
	app := newDummyApp()
	babel := flaskbabel.NewBabel()
	babel.InitApp(app)
	config := app.Extensions["babel"]
	assert.NotNil(t, config)
	assert.Equal(t, "en", getConfigDefaultLocale(config))
	assert.Equal(t, "messages", getConfigDefaultDomain(config))
	assert.NotNil(t, getConfigTranslationDirectories(config))
	assert.Equal(t, babel, getConfigInstance(config))
}

func TestBabelInitAppConfigOptionsOverride(t *testing.T) {
	app := newDummyApp()
	app.Config["BABEL_DEFAULT_LOCALE"] = "fr"
	app.Config["BABEL_DOMAIN"] = "customdomain"
	app.Config["BABEL_TRANSLATION_DIRECTORIES"] = "foo;bar"
	babel := flaskbabel.NewBabel()
	babel.InitApp(app)
	config := app.Extensions["babel"]
	assert.Equal(t, "fr", getConfigDefaultLocale(config))
	assert.Equal(t, "customdomain", getConfigDefaultDomain(config))
	assert.ElementsMatch(t, []string{"foo", "bar"}, getConfigDefaultDirectories(config))
}

func TestBabelInitAppWithSelectors(t *testing.T) {
	app := newDummyApp()
	selector := func() string { return "de" }
	babel := flaskbabel.NewBabel()
	babel.InitApp(app, selector, selector)
	config := app.Extensions["babel"]
	assert.Equal(t, "de", callLocaleSelector(config))
	assert.Equal(t, "de", callTimezoneSelector(config))
}

func TestGetBabel(t *testing.T) {
	app := newDummyApp()
	babel := flaskbabel.NewBabel()
	babel.InitApp(app)
	config, err := flaskbabel.GetBabel(app)
	assert.NotNil(t, config)
	assert.Nil(t, err)
	_, err = flaskbabel.GetBabel(nil)
	assert.True(t, errors.Is(err, flaskbabel.ErrNoCurrentApp))
}

func TestDefaultDateFormatsDefined(t *testing.T) {
	babel := flaskbabel.NewBabel()
	d := babel.GetDefaultDateFormats()
	assert.NotNil(t, d)
	assert.Equal(t, "medium", d["datetime"])
}