package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

type PublicDummyApp struct {
	Config     map[string]interface{}
	Extensions map[string]interface{}
}

func newPublicDummyApp() *PublicDummyApp {
	return &PublicDummyApp{
		Config:     map[string]interface{}{},
		Extensions: map[string]interface{}{},
	}
}

func TestPublicBabelInitAndAppProperties(t *testing.T) {
	app := newPublicDummyApp()
	babel := flaskbabel.NewBabel()
	babel.InitApp(app)
	config := app.Extensions["babel"]
	assert.NotNil(t, config)
	assert.Equal(t, "en", getConfigDefaultLocale(config))
	assert.Equal(t, "messages", getConfigDefaultDomain(config))
	assert.NotNil(t, getConfigTranslationDirectories(config))
	assert.Equal(t, babel, getConfigInstance(config))
}

func TestPublicBabelInitAppConfigOptionsOverride(t *testing.T) {
	app := newPublicDummyApp()
	app.Config["BABEL_DEFAULT_LOCALE"] = "es"
	app.Config["BABEL_DOMAIN"] = "alt_domain"
	app.Config["BABEL_TRANSLATION_DIRECTORIES"] = "alpha;beta"
	babel := flaskbabel.NewBabel()
	babel.InitApp(app)
	config := app.Extensions["babel"]
	assert.Equal(t, "es", getConfigDefaultLocale(config))
	assert.Equal(t, "alt_domain", getConfigDefaultDomain(config))
	assert.ElementsMatch(t, []string{"alpha", "beta"}, getConfigDefaultDirectories(config))
}

func TestPublicBabelInitAppWithSelectors(t *testing.T) {
	app := newPublicDummyApp()
	selector := func() string { return "it" }
	babel := flaskbabel.NewBabel()
	babel.InitApp(app, selector, selector)
	config := app.Extensions["babel"]
	assert.Equal(t, "it", callLocaleSelector(config))
	assert.Equal(t, "it", callTimezoneSelector(config))
}

func TestPublicGetBabel(t *testing.T) {
	app := newPublicDummyApp()
	babel := flaskbabel.NewBabel()
	babel.InitApp(app)
	config, err := flaskbabel.GetBabel(app)
	assert.NotNil(t, config)
	assert.Nil(t, err)
	_, err = flaskbabel.GetBabel(nil)
	assert.True(t, errors.Is(err, flaskbabel.ErrNoCurrentApp))
}

func TestPublicDefaultDateFormatsDefined(t *testing.T) {
	babel := flaskbabel.NewBabel()
	d := babel.GetDefaultDateFormats()
	assert.NotNil(t, d)
	assert.Equal(t, "medium", d["date"])
}