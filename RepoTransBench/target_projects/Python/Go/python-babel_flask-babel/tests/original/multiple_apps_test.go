package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestMultipleApps(t *testing.T) {
	b := flaskbabel.NewBabel()

	app1 := &TestApp{}
	b.InitApp(app1, "de_DE")

	app2 := &TestApp{}
	b.InitApp(app2, "en_US")

	withTestRequestContext(app1, func() {
		assert.Equal(t, "de_DE", flaskbabel.GetLocale())
		assert.Equal(t, "Hallo Peter!", flaskbabel.Gettext("Hello %(name)s!", "Peter"))
	})

	withTestRequestContext(app2, func() {
		assert.Equal(t, "en_US", flaskbabel.GetLocale())
		assert.Equal(t, "Hello Peter!", flaskbabel.Gettext("Hello %(name)s!", "Peter"))
	})
}