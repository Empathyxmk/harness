package public_tests

import (
	"testing"
	"time"
	"github.com/stretchr/testify/assert"
	"myusuf3_delorean/delorean"
)

func TestDeloreanConstructorNaivePublic(t *testing.T) {
	dt := time.Date(2022, 7, 14, 19, 15, 11, 0, time.UTC)
	d := delorean.NewDelorean(dt, "Asia/Singapore")
	assert.Equal(t, 2022, d.Datetime().Year())
	assert.Equal(t, 7, int(d.Datetime().Month()))
	assert.Equal(t, 14, d.Datetime().Day())
	assert.Contains(t, d.TZ().String(), "Asia/Singapore")
}

func TestDeloreanConstructorAwarePublic(t *testing.T) {
	location, _ := time.LoadLocation("Australia/Sydney")
	dt := time.Date(2023, 1, 25, 23, 30, 3, 0, location)
	d := delorean.NewDelorean(dt, "")
	assert.Equal(t, 2023, d.Datetime().Year())
	assert.Equal(t, 1, int(d.Datetime().Month()))
	assert.Equal(t, 25, d.Datetime().Day())
	assert.Contains(t, d.TZ().String(), "Sydney")
}

func TestDeloreanStrPublic(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2021, 5, 8, 20, 48, 0, 0, time.UTC), "America/Mexico_City")
	s := d.String()
	assert.Contains(t, s, "Delorean")
	assert.Contains(t, s, "Mexico")
}

func TestParseStringPublic(t *testing.T) {
	d := delorean.Parse("2024-01-12T13:22:05-04:00")
	assert.Equal(t, 2024, d.Datetime().Year())
	assert.Equal(t, 1, int(d.Datetime().Month()))
	assert.Equal(t, 12, d.Datetime().Day())
	assert.Equal(t, 13, d.Datetime().Hour())
	assert.NotNil(t, d.TZ())
}

func TestParseUnixEpochPublic(t *testing.T) {
	ts := int64(1640995200)
	d := delorean.Epoch(ts, "")
	assert.Equal(t, 2022, d.Datetime().Year())
	assert.Equal(t, 1, int(d.Datetime().Month()))
	assert.Equal(t, 1, d.Datetime().Day())
	assert.Contains(t, d.TZ().String(), "UTC")
}

func TestUTCNowPublic(t *testing.T) {
	d := delorean.UTCNow()
	now := time.Now().UTC()
	diff := d.Datetime().Sub(now).Seconds()
	assert.Less(t, diff, 5.0)
	assert.Contains(t, d.TZ().String(), "UTC")
}

func TestShiftPublic(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2031, 2, 14, 21, 32, 0, 0, time.UTC), "Asia/Dubai")
	d2 := d.Shift("Europe/London")
	assert.Contains(t, d2.TZ().String(), "London")
	assert.Equal(t, 2031, d2.Datetime().Year())
	assert.Equal(t, 2, int(d2.Datetime().Month()))
}

func TestTruncatePublic(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2019, 4, 15, 16, 14, 59, 0, time.UTC), "US/Pacific")
	d2 := d.Truncate("month")
	assert.Equal(t, 2019, d2.Datetime().Year())
	assert.Equal(t, 4, int(d2.Datetime().Month()))
	assert.Equal(t, 1, d2.Datetime().Day())
}

func TestNextPreviousPublic(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2017, 6, 12, 21, 30, 0, 0, time.UTC), "Europe/Bucharest")
	nex := d.Next("month")
	prev := d.Last("month")
	assert.Equal(t, 7, int(nex.Datetime().Month()))
	assert.Equal(t, 5, int(prev.Datetime().Month()))
}

func TestInvalidTimezonePublic(t *testing.T) {
	_, err := delorean.NewDelorean(time.Date(2021, 8, 31, 0, 0, 0, 0, time.UTC), "Never/Neverland")
	assert.Error(t, err)
}

func TestInvalidTimePublic(t *testing.T) {
	_, err := delorean.ParseWithErr("not-a-time-string-xyz")
	assert.Error(t, err)
}

func TestComparisonsPublic(t *testing.T) {
	d1 := delorean.NewDelorean(time.Date(2011, 11, 11, 0, 0, 0, 0, time.UTC), "UTC")
	d2 := delorean.NewDelorean(time.Date(2012, 12, 10, 0, 0, 0, 0, time.UTC), "UTC")
	assert.True(t, d1.Less(d2))
	assert.True(t, d2.Greater(d1))
	assert.False(t, d1.Equals(d2))
}

func TestEqualityTimezonePublic(t *testing.T) {
	d1 := delorean.NewDelorean(time.Date(2008, 8, 8, 0, 0, 0, 0, time.UTC), "Asia/Shanghai")
	d2 := delorean.NewDelorean(time.Date(2008, 8, 8, 0, 0, 0, 0, time.UTC), "Asia/Shanghai")
	assert.True(t, d1.Equals(d2))
}

func TestAddSubtractTimedeltaPublic(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2010, 12, 1, 10, 11, 0, 0, time.UTC), "Europe/Istanbul")
	d2 := d.AddDays(3)
	d3 := d2.AddHours(-12)
	assert.Equal(t, 4, d2.Datetime().Day())
	assert.Equal(t, 3, d3.Datetime().Day())
	assert.Equal(t, 22, d3.Datetime().Hour())
}

func TestMinMaxPublic(t *testing.T) {
	d1 := delorean.NewDelorean(time.Date(2017, 6, 1, 8, 0, 0, 0, time.UTC), "Europe/Helsinki")
	d2 := delorean.NewDelorean(time.Date(2017, 6, 2, 8, 0, 0, 0, time.UTC), "Europe/Helsinki")
	tests := []delorean.Delorean{d1, d2}
	var min, max delorean.Delorean = d1, d1
	for _, d := range tests {
		if d.Datetime().Before(min.Datetime()) {
			min = d
		}
		if d.Datetime().After(max.Datetime()) {
			max = d
		}
	}
	assert.True(t, max.Equals(d2))
	assert.True(t, min.Equals(d1))
}