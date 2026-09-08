package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"myusuf3_delorean/delorean"
)

func TestDeloreanConstructorNaive(t *testing.T) {
	// dt = datetime(2022, 1, 2, 12, 0, 0)
	dt := time.Date(2022, time.January, 2, 12, 0, 0, 0, time.UTC)
	d := delorean.NewDelorean(dt, "UTC")
	assert.True(t, d.Datetime().Equal(dt))
	assert.Equal(t, "UTC", d.TZ().String())
}

func TestDeloreanConstructorTimezoneStrAndObj(t *testing.T) {
	dt := time.Date(2022, time.January, 2, 13, 0, 0, 0, time.UTC)
	d1 := delorean.NewDelorean(dt, "US/Pacific")
	assert.Equal(t, "US/Pacific", d1.TZ().String())
	// Simulate obj as string as Go doesn't have pytz obj style
	d2 := delorean.NewDelorean(dt, "US/Eastern")
	assert.Equal(t, "US/Eastern", d2.TZ().String())
}

func TestDeloreanConstructorInvalidTimezone(t *testing.T) {
	dt := time.Date(2022, time.January, 2, 13, 0, 0, 0, time.UTC)
	_, err := delorean.NewDelorean(dt, "Invalid/Zone")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Invalid/Zone")
}

func TestDeloreanShiftMinutesAndSeconds(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2017, 5, 6, 12, 30, 0, 0, time.UTC), "UTC")
	d2 := d.ShiftMinutesSeconds(2, 5)
	assert.Equal(t, 32, d2.Datetime().Minute())
	assert.Equal(t, 5, d2.Datetime().Second())
}

func TestDeloreanNextLastMethods(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2021, 12, 31, 23, 0, 0, 0, time.UTC), "UTC")
	nextDay := d.NextDay()
	assert.True(t, nextDay.Datetime().Day() == 1 || nextDay.Datetime().Month() == time.January)

	lastWeek := d.LastWeek()
	daysDiff := int(d.Datetime().Sub(lastWeek.Datetime()).Hours()) / 24
	assert.True(t, daysDiff >= 0 && daysDiff <= 7)
}

func TestDeloreanTruncateToDay(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2022, 3, 4, 15, 34, 56, 0, time.UTC), "UTC")
	truncated := d.Truncate("day")
	assert.Equal(t, 0, truncated.Datetime().Hour())
	assert.Equal(t, 0, truncated.Datetime().Minute())
}

func TestDeloreanEqAndRepr(t *testing.T) {
	d1 := delorean.NewDelorean(time.Date(2022, 3, 4, 0, 0, 0, 0, time.UTC), "UTC")
	d2 := delorean.NewDelorean(time.Date(2022, 3, 4, 0, 0, 0, 0, time.UTC), "UTC")
	assert.True(t, d1.Equals(d2))
	assert.Contains(t, d1.String(), "Delorean")
}

func TestDeloreanRollforwardRollbackup(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2022, 3, 6, 0, 0, 0, 0, time.UTC), "UTC")
	rf := d.Rollforward("Monday")
	rb := d.Rollback("Monday")
	assert.NotNil(t, rf.Datetime())
	assert.NotNil(t, rb.Datetime())
	assert.False(t, rf.Equals(d) && rb.Equals(d))
}

func TestDeloreanTimezoneAndConvert(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2021, 3, 1, 10, 0, 0, 0, time.UTC), "UTC")
	local := d.Localize("US/Pacific")
	assert.Equal(t, "US/Pacific", local.TZ().String())
	norm := d.Normalize("US/Pacific")
	assert.Equal(t, "US/Pacific", norm.TZ().String())
	unix := d.ToUnix()
	assert.IsType(t, float64(0), unix)
	assert.NotNil(t, d.ToUTC())
	assert.NotNil(t, d.ToDatetime())
}

func TestDeloreanConvertUnsupported(t *testing.T) {
	d := delorean.NewDelorean(time.Date(2022, 1, 1, 0, 0, 0, 0, time.UTC), "UTC")
	_, err := d.TruncateWithErr("unknown")
	assert.Error(t, err)
}

func TestDeloreanFactoryMethods(t *testing.T) {
	d1 := delorean.UTCNow()
	d2 := delorean.Now("UTC")
	d3 := delorean.Parse("2021-01-01T10:00:00Z")
	d4 := delorean.Epoch(0, "UTC")
	assert.NotNil(t, d1)
	assert.NotNil(t, d2)
	assert.NotNil(t, d3)
	assert.NotNil(t, d4)
	assert.Equal(t, 1970, d4.Datetime().Year())
}