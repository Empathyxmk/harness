package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"myusuf3_delorean/delorean"
)

func TestGetTotalSecondBasicHtmlcov(t *testing.T) {
	td := time.Duration(24*time.Hour + 1*time.Second + 1*time.Microsecond)
	total := delorean.GetTotalSecond(td)
	expect := float64(1*24*3600 + 1 + 1e-6)
	assert.InDelta(t, expect, total, 1e-6)
}

func TestIsDatetimeNaiveHtmlcov(t *testing.T) {
	dt := time.Now()
	assert.True(t, delorean.IsDatetimeNaive(dt))
	dtAware := dt.In(time.UTC)
	assert.False(t, delorean.IsDatetimeNaive(dtAware))
}

func TestIsDatetimeInstanceNoneHtmlcov(t *testing.T) {
	assert.Nil(t, delorean.IsDatetimeInstance(nil))
}

func TestIsDatetimeInstanceWrongTypeHtmlcov(t *testing.T) {
	_, err := delorean.IsDatetimeInstance(123)
	assert.Error(t, err)
}

func TestMoveDatetimeDayHtmlcov(t *testing.T) {
	dt := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeDay(dt, "next", 5)
	assert.Equal(t, 6, result.Day())
	result2 := delorean.MoveDatetimeDay(dt, "last", 1)
	assert.True(t, result2.Day() == 31 || result2.Month() == time.December)
}

func TestMoveDatetimeHourHtmlcov(t *testing.T) {
	dt := time.Date(2020, 1, 1, 4, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeHour(dt, "next", 2)
	assert.Equal(t, 6, result.Hour())
	result2 := delorean.MoveDatetimeHour(dt, "last", 3)
	assert.Equal(t, 1, result2.Hour())
}

func TestMoveDatetimeMinuteHtmlcov(t *testing.T) {
	dt := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeMinute(dt, "next", 45)
	assert.Equal(t, 45, result.Minute())
}

func TestMoveDatetimeSecondHtmlcov(t *testing.T) {
	dt := time.Date(2020, 1, 1, 0, 0, 30, 0, time.UTC)
	result := delorean.MoveDatetimeSecond(dt, "next", 29)
	assert.Equal(t, 59, result.Second())
}

func TestMoveDatetimeMonthHtmlcov(t *testing.T) {
	dt := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeMonth(dt, "next", 2)
	assert.Equal(t, time.March, result.Month())
	result2 := delorean.MoveDatetimeMonth(dt, "last", 1)
	assert.True(t, result2.Month() == time.December && result2.Year() == 2019)
}

func TestMoveDatetimeWeekHtmlcov(t *testing.T) {
	dt := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeWeek(dt, "next", 2)
	assert.Contains(t, []int{8, 15}, result.Day())
}

func TestMoveDatetimeYearHtmlcov(t *testing.T) {
	dt := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeYear(dt, "next", 2)
	assert.Equal(t, 2022, result.Year())
	result2 := delorean.MoveDatetimeYear(dt, "last", 1)
	assert.Equal(t, 2019, result2.Year())
}

func TestMoveDatetimeNamedDayHtmlcov(t *testing.T) {
	type DayTest struct {
		Current      string
		Target       string
		Direction    string
		ExpectedDays int
	}
	tests := []DayTest{
		{"Monday", "Tuesday", "next", 7},
		{"Saturday", "Monday", "next", 1},
		{"Friday", "Wednesday", "last", -3},
		{"Wednesday", "Wednesday", "next", 6},
		{"Sunday", "Friday", "last", -3},
	}
	dayMap := map[string]int{
		"Monday": 6, "Tuesday": 7, "Wednesday": 8, "Thursday": 9, "Friday": 10, "Saturday": 11, "Sunday": 12,
	}
	for _, test := range tests {
		dt := time.Date(2021, 4, dayMap[test.Current], 0, 0, 0, 0, time.UTC)
		moved := delorean.MoveDatetimeNamedDay(dt, test.Direction, test.Target)
		diff := int(moved.Sub(dt).Hours() / 24)
		assert.Equal(t, test.ExpectedDays, diff)
	}
}

func TestDatetimeTimezoneAndLocalizeNormalizeHtmlcov(t *testing.T) {
	result := delorean.DatetimeTimezone("US/Pacific")
	assert.NotNil(t, result.Location())
	naive := time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC)
	aware := delorean.Localize(naive, "UTC")
	assert.NotNil(t, aware.Location())
	aware2 := delorean.Localize(naive, "UTC")
	assert.NotNil(t, aware2.Location())
}

func TestNormalizeValidHtmlcov(t *testing.T) {
	d1 := time.Date(2021, 1, 1, 0, 0, 0, 0, time.UTC)
	normalized := delorean.Normalize(d1, "US/Pacific")
	assert.Contains(t, normalized.Location().String(), "Pacific")
}

func TestNormalizeInvalidTimezoneHtmlcov(t *testing.T) {
	d1 := time.Date(2021, 1, 1, 0, 0, 0, 0, time.UTC)
	_, err := delorean.NormalizeWithErr(d1, "Invalid/Zone")
	assert.Error(t, err)
}