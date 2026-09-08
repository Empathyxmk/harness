package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestPublicForceLocaleContextManager(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)

	withTestRequestContext(app, func() {
		b.ForceLocale("it", func() {
			assert.Equal(t, "it", flaskbabel.GetLocale())
		})
		assert.Equal(t, "en", flaskbabel.GetLocale())
	})
}

func TestPublicForceLocaleNested(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app, "fr")
	withTestRequestContext(app, func() {
		b.ForceLocale("ja", func() {
			assert.Equal(t, "ja", flaskbabel.GetLocale())
			b.ForceLocale("de", func() {
				assert.Equal(t, "de", flaskbabel.GetLocale())
			})
			assert.Equal(t, "ja", flaskbabel.GetLocale())
		})
		assert.Equal(t, "fr", flaskbabel.GetLocale())
	})
}