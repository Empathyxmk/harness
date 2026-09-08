package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"myusuf3_delorean/delorean"
)

// A helper for time equality with location normalization.
func datetimesEqual(t1, t2 time.Time) bool {
	return t1.Equal(t2)
}

func TestDeloreanConstructorNaiveHtmlcov(t *testing.T) {
	dt := time.Date(2022, 1, 2, 12, 0, 0, 0, time.UTC)
	d, err := delorean.NewDelorean(dt, "UTC")
	assert.NoError(t, err)
	loc, _ := time.LoadLocation("UTC")
	expected := time.Date(2022, 1, 2, 12, 0, 0, 0, loc)
	assert.True(t, datetimesEqual(d.Datetime, expected))
	assert.Equal(t, "UTC", d.Timezone)
}

func TestDeloreanConstructorTimezoneStrAndObjHtmlcov(t *testing.T) {
	dt := time.Date(2022, 1, 2, 13, 0, 0, 0, time.UTC)
	d1, err := delorean.NewDelorean(dt, "US/Pacific")
	assert.NoError(t, err)
	assert.Equal(t, "US/Pacific", d1.Timezone)
	// "Timezone obj" emulation: Delorean always accepts a string for Go implementation
	d2, err := delorean.NewDelorean(dt, "US/Eastern")
	assert.NoError(t, err)
	assert.Equal(t, "US/Eastern", d2.Timezone)
}

func TestDeloreanConstructorInvalidTimezoneHtmlcov(t *testing.T) {
	dt := time.Date(2022, 1, 2, 13, 0, 0, 0, time.UTC)
	_, err := delorean.NewDelorean(dt, "Invalid/Zone")
	assert.Error(t, err)
}

func TestDeloreanShiftMinutesAndSecondsHtmlcov(t *testing.T) {
	d, err := delorean.NewDelorean(time.Date(2017, 5, 6, 12, 30, 0, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	d2 := d.Shift(0, 2, 5) // Shift by 2 minutes, 5 seconds
	assert.Equal(t, 32, d2.Datetime.Minute())
	assert.Equal(t, 5, d2.Datetime.Second())
}

func TestDeloreanNextLastMethodsHtmlcov(t *testing.T) {
	d, err := delorean.NewDelorean(time.Date(2021, 12, 31, 23, 0, 0, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	nextDay := d.NextDay()
	assert.True(t, nextDay.Datetime.Day() == 1 || nextDay.Datetime.Month() == time.January)
	lastWeek := d.LastWeek()
	daydelta := int(d.Datetime.Sub(lastWeek.Datetime).Hours() / 24)
	assert.True(t, 0 <= daydelta && daydelta <= 7)
}

func TestDeloreanTruncateToDayHtmlcov(t *testing.T) {
	d, err := delorean.NewDelorean(time.Date(2022, 3, 4, 15, 34, 56, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	truncated, err := d.Truncate("day")
	assert.NoError(t, err)
	assert.Equal(t, 0, truncated.Datetime.Hour())
	assert.Equal(t, 0, truncated.Datetime.Minute())
}

func TestDeloreanEqAndReprHtmlcov(t *testing.T) {
	d1, err := delorean.NewDelorean(time.Date(2022, 3, 4, 0, 0, 0, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	d2, err := delorean.NewDelorean(time.Date(2022, 3, 4, 0, 0, 0, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	assert.True(t, d1.Equal(d2))
	assert.Contains(t, d1.String(), "Delorean")
}

func TestDeloreanRollforwardRollbackHtmlcov(t *testing.T) {
	d, err := delorean.NewDelorean(time.Date(2022, 3, 6, 0, 0, 0, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	rf := d.Rollforward("Monday")
	rb := d.Rollback("Monday")
	assert.NotNil(t, rf.Datetime)
	assert.NotNil(t, rb.Datetime)
	assert.True(t, !(rf.Equal(*d)) || !(rb.Equal(*d)))
}

func TestDeloreanTimezoneAndConvertHtmlcov(t *testing.T) {
	d, err := delorean.NewDelorean(time.Date(2021, 3, 1, 10, 0, 0, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	local, err := d.Localize("US/Pacific")
	assert.NoError(t, err)
	assert.Equal(t, "US/Pacific", local.Timezone)
	norm, err := d.Normalize("US/Pacific")
	assert.NoError(t, err)
	assert.Equal(t, "US/Pacific", norm.Timezone)
	assert.IsType(t, float64(0), d.ToUnix())
	assert.NotNil(t, d.ToTime().Location())
}

func TestDeloreanConvertUnsupportedHtmlcov(t *testing.T) {
	d, err := delorean.NewDelorean(time.Date(2022, 1, 1, 0, 0, 0, 0, time.UTC), "UTC")
	assert.NoError(t, err)
	_, err = d.Truncate("unknown")
	assert.Error(t, err)
}

func TestDeloreanFactoryMethodsHtmlcov(t *testing.T) {
	d1 := delorean.UtcNow()
	d2, err := delorean.Now("UTC")
	assert.NoError(t, err)
	d3, err := delorean.Parse("2021-01-01T10:00:00Z")
	assert.NoError(t, err)
	d4, err := delorean.Epoch(0, "UTC")
	assert.NoError(t, err)
	assert.True(t, d1 != nil)
	assert.True(t, d2 != nil)
	assert.True(t, d3 != nil)
	assert.True(t, d4 != nil)
	assert.Equal(t, 1970, d4.Datetime.Year())
}