package public_tests

import (
	"testing"
	"time"
	"github.com/stretchr/testify/assert"
	"myusuf3_delorean/delorean"
)

func TestGetTotalSecondBasicPublic(t *testing.T) {
	td := time.Duration(3*time.Hour + 4*time.Minute + 5*time.Second + 8*time.Microsecond)
	expected := float64(3*3600 + 4*60 + 5 + 8e-6)
	total := delorean.GetTotalSecond(td)
	assert.InDelta(t, expected, total, 1e-6)
}

func TestIsDatetimeNaivePublic(t *testing.T) {
	dt := time.Date(2005, 10, 11, 0, 0, 0, 0, time.UTC)
	assert.True(t, delorean.IsDatetimeNaive(dt))
	dtAware := dt.In(time.UTC)
	assert.False(t, delorean.IsDatetimeNaive(dtAware))
}

func TestIsDatetimeInstanceNonePublic(t *testing.T) {
	assert.Nil(t, delorean.IsDatetimeInstance(nil))
}

func TestIsDatetimeInstanceWrongTypePublic(t *testing.T) {
	_, err := delorean.IsDatetimeInstance("not-a-datetime")
	assert.Error(t, err)
}

func TestMoveDatetimeDayPublic(t *testing.T) {
	dt := time.Date(2022, 6, 15, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeDay(dt, "next", 10)
	assert.Equal(t, 25, result.Day())
	result2 := delorean.MoveDatetimeDay(dt, "last", 3)
	assert.Equal(t, 12, result2.Day())
}

func TestMoveDatetimeHourPublic(t *testing.T) {
	dt := time.Date(2023, 2, 15, 13, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeHour(dt, "next", 8)
	assert.Equal(t, 21, result.Hour())
	result2 := delorean.MoveDatetimeHour(dt, "last", 5)
	assert.Equal(t, 8, result2.Hour())
}

func TestMoveDatetimeMinutePublic(t *testing.T) {
	dt := time.Date(2022, 7, 4, 9, 10, 0, 0, time.UTC)
	result := delorean.MoveDatetimeMinute(dt, "next", 35)
	assert.Equal(t, 45, result.Minute())
}

func TestMoveDatetimeSecondPublic(t *testing.T) {
	dt := time.Date(2021, 9, 20, 1, 5, 15, 0, time.UTC)
	result := delorean.MoveDatetimeSecond(dt, "next", 40)
	assert.Equal(t, 55, result.Second())
}

func TestMoveDatetimeMonthPublic(t *testing.T) {
	dt := time.Date(2017, 11, 18, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeMonth(dt, "next", 5)
	assert.Equal(t, 4, int(result.Month()))
	assert.Equal(t, 2018, result.Year())
	result2 := delorean.MoveDatetimeMonth(dt, "last", 1)
	assert.Equal(t, 10, int(result2.Month()))
	assert.Equal(t, 2017, result2.Year())
}

func TestMoveDatetimeWeekPublic(t *testing.T) {
	dt := time.Date(2021, 3, 10, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeWeek(dt, "next", 3)
	assert.Contains(t, []int{17, 24, 31}, result.Day())
}

func TestMoveDatetimeYearPublic(t *testing.T) {
	dt := time.Date(2018, 12, 31, 0, 0, 0, 0, time.UTC)
	result := delorean.MoveDatetimeYear(dt, "next", 4)
	assert.Equal(t, 2022, result.Year())
	result2 := delorean.MoveDatetimeYear(dt, "last", 2)
	assert.Equal(t, 2016, result2.Year())
}

func TestMoveDatetimeNamedDayPublic(t *testing.T) {
	type namedDayTest struct {
		Current      string
		Target       string
		Direction    string
		ExpectedDays int
	}
	tests := []namedDayTest{
		{"Monday", "Thursday", "next", 3},
		{"Wednesday", "Monday", "last", -2},
		{"Saturday", "Saturday", "next", 7},
		{"Sunday", "Friday", "last", -2},
	}
	dayMap := map[string]int{"Monday": 10, "Tuesday": 11, "Wednesday": 12, "Thursday": 13, "Friday": 14, "Saturday": 15, "Sunday": 16}
	for _, test := range tests {
		dt := time.Date(2022, 1, dayMap[test.Current], 0, 0, 0, 0, time.UTC)
		moved := delorean.MoveDatetimeNamedDay(dt, test.Direction, test.Target)
		daysDiff := int(moved.Sub(dt).Hours() / 24)
		assert.Equal(t, test.ExpectedDays, daysDiff)
	}
}

func TestDatetimeTimezoneAndLocalizeNormalizePublic(t *testing.T) {
	result := delorean.DatetimeTimezone("Europe/Berlin")
	assert.NotNil(t, result.Location())
	naive := time.Date(2015, 12, 3, 0, 0, 0, 0, time.UTC)
	aware := delorean.Localize(naive, "US/Eastern")
	assert.NotNil(t, aware.Location())
	aware2 := delorean.Localize(naive, "US/Eastern")
	assert.NotNil(t, aware2.Location())
}

func TestNormalizeValidPublic(t *testing.T) {
	d1 := time.Date(2018, 5, 5, 0, 0, 0, 0, time.FixedZone("Europe/London", 0))
	normalized := delorean.Normalize(d1, "US/Eastern")
	assert.Contains(t, normalized.Location().String(), "Eastern")
}

func TestNormalizeInvalidTimezonePublic(t *testing.T) {
	d1 := time.Date(2020, 3, 17, 0, 0, 0, 0, time.UTC)
	_, err := delorean.NormalizeWithErr(d1, "No/ExistZone")
	assert.Error(t, err)
}