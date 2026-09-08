package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestDateFormattingBasics(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	d := time.Date(2010, 4, 12, 13, 46, 0, 0, time.UTC)
	delta := 6 * 24 * time.Hour

	withTestRequestContext(app, func() {
		assert.Equal(t, "Apr 12, 2010, 1:46:00 PM", b.FormatDatetime(d))
		assert.Equal(t, "Apr 12, 2010", b.FormatDate(d))
		assert.Equal(t, "1:46:00 PM", b.FormatTime(d))
		assert.Equal(t, "1 week", b.FormatTimedelta(delta))
		assert.Equal(t, "6 days", b.FormatTimedelta(delta, 1))
	})

	withTestRequestContext(app, func() {
		b.SetDefaultTimezone("Europe/Vienna")
		assert.Equal(t, "Apr 12, 2010, 3:46:00 PM", b.FormatDatetime(d))
		assert.Equal(t, "Apr 12, 2010", b.FormatDate(d))
		assert.Equal(t, "3:46:00 PM", b.FormatTime(d))
	})

	withTestRequestContext(app, func() {
		b.SetDefaultLocale("de_DE")
		assert.Equal(t, "12. April 2010, 15:46:00 MESZ", b.FormatDatetime(d, "long"))
	})
}

func TestDateFormattingCustomFormats(t *testing.T) {
	app := &TestApp{}
	app.Config = map[string]interface{}{
		"BABEL_DEFAULT_LOCALE":   "en_US",
		"BABEL_DEFAULT_TIMEZONE": "Pacific/Johnston",
	}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	b.SetDateFormat("datetime", "long")
	b.SetDateFormat("datetime.long", "MMMM d, yyyy h:mm:ss a")

	d := time.Date(2010, 4, 12, 13, 46, 0, 0, time.UTC)

	withTestRequestContext(app, func() {
		assert.Equal(t, "April 12, 2010 3:46:00 AM", b.FormatDatetime(d))
	})
}

func TestDateFormattingCustomLocaleSelector(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)

	d := time.Date(2010, 4, 12, 13, 46, 0, 0, time.UTC)
	theTimezone := "UTC"
	theLocale := "en_US"

	selectLocale := func() string { return theLocale }
	selectTimezone := func() string { return theTimezone }

	b.SetLocaleSelector(selectLocale)
	b.SetTimezoneSelector(selectTimezone)

	withTestRequestContext(app, func() {
		assert.Equal(t, "Apr 12, 2010, 1:46:00 PM", b.FormatDatetime(d))
	})

	theLocale = "de_DE"
	theTimezone = "Europe/Vienna"

	withTestRequestContext(app, func() {
		assert.Equal(t, "12.04.2010, 15:46:00", b.FormatDatetime(d))
	})
}

func TestDateFormattingRefreshing(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)

	d := time.Date(2010, 4, 12, 13, 46, 0, 0, time.UTC)
	withTestRequestContext(app, func() {
		assert.Equal(t, "Apr 12, 2010, 1:46:00 PM", b.FormatDatetime(d))
		b.SetDefaultTimezone("Europe/Vienna")
		b.Refresh()
		assert.Equal(t, "Apr 12, 2010, 3:46:00 PM", b.FormatDatetime(d))
	})
}