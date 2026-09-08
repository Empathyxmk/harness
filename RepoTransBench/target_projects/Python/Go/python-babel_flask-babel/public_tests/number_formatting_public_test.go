package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestPublicFormatDecimal(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	withTestRequestContext(app, func() {
		val := b.FormatDecimal(8142.73)
		assert.NotEmpty(t, val)
	})
}

func TestPublicFormatCurrency(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	withTestRequestContext(app, func() {
		result := b.FormatCurrency(99.95, "EUR")
		assert.NotEmpty(t, result)
	})
}

func TestPublicFormatPercent(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	withTestRequestContext(app, func() {
		percent := b.FormatPercent(3.5)
		assert.NotEmpty(t, percent)
	})
}

func TestPublicFormatScientific(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	withTestRequestContext(app, func() {
		sci := b.FormatScientific(987654)
		assert.NotEmpty(t, sci)
	})
}