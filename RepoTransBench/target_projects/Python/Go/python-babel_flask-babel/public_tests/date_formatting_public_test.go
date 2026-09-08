package public_tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestPublicFormatTime(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	dt := time.Date(2021, 8, 14, 22, 15, 30, 0, time.UTC)
	withTestRequestContext(app, func() {
		s := b.FormatTime(dt, "short")
		assert.NotEmpty(t, s)
	})
}

func TestPublicFormatDate(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	dd := time.Date(2022, 7, 20, 0, 0, 0, 0, time.UTC)
	withTestRequestContext(app, func() {
		s := b.FormatDate(dd, "long")
		assert.NotEmpty(t, s)
	})
}

func TestPublicFormatDatetime(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	dd := time.Date(2020, 12, 31, 19, 45, 16, 0, time.UTC)
	withTestRequestContext(app, func() {
		s := b.FormatDatetime(dd, "full")
		assert.NotEmpty(t, s)
	})
}

func TestPublicFormatTimedelta(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	delta := 3*24*time.Hour + time.Hour + 25*time.Minute
	withTestRequestContext(app, func() {
		s := b.FormatTimedelta(delta)
		assert.NotEmpty(t, s)
	})
}

func TestPublicFormatTimeCustomLocale(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	dt := time.Date(2023, 6, 15, 17, 40, 0, 0, time.UTC)
	withTestRequestContext(app, func() {
		s := b.FormatTime(dt, "short", "it")
		assert.NotEmpty(t, s)
	})
}