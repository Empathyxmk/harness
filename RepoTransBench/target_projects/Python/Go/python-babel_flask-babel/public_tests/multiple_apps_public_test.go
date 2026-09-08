package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestPublicMultipleApps(t *testing.T) {
	b := flaskbabel.NewBabel()

	app1 := &TestApp{}
	b.InitApp(app1, "fr_FR")
	app2 := &TestApp{}
	b.InitApp(app2, "it_IT")

	withTestRequestContext(app1, func() {
		assert.Equal(t, "fr_FR", flaskbabel.GetLocale())
		assert.Equal(t, "Welcome Marie!", flaskbabel.Gettext("Welcome %(user)s!", "Marie"))
	})

	withTestRequestContext(app2, func() {
		assert.Equal(t, "it_IT", flaskbabel.GetLocale())
		assert.Equal(t, "Welcome Luca!", flaskbabel.Gettext("Welcome %(user)s!", "Luca"))
	})
}