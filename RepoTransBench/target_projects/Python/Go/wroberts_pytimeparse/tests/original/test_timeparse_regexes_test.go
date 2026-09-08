package original

import (
	"regexp"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestWeeksRegex(t *testing.T) {
	pattern := `^(?P<weeks>(\d+(\.\d+)?))\s*(w|wk|wks|weeks?)`
	for _, val := range []string{"2w", "2wk", "2wks", "2weeks"} {
		re := regexp.MustCompile(pattern)
		m := re.FindStringSubmatch(val)
		require.NotNil(t, m)
		require.NotEmpty(t, m[1])
	}
}

func TestDaysRegex(t *testing.T) {
	pattern := `^(?P<days>(\d+(\.\d+)?))\s*(d|dy|dys|days?)`
	for _, val := range []string{"4d", "4dy", "4dys", "4days"} {
		re := regexp.MustCompile(pattern)
		m := re.FindStringSubmatch(val)
		require.NotNil(t, m)
		require.NotEmpty(t, m[1])
	}
	re := regexp.MustCompile(pattern)
	match := re.FindStringSubmatch("1.5days")
	require.NotNil(t, match)
	require.Contains(t, match[0], "1.5")
}

func TestHoursRegex(t *testing.T) {
	pattern := `^(?P<hours>(\d+(\.\d+)?))\s*(h|hr|hrs|hour|hours?)`
	for _, val := range []string{"7h", "7hr", "7hrs", "7hour", "7hours"} {
		re := regexp.MustCompile(pattern)
		m := re.FindStringSubmatch(val)
		require.NotNil(t, m)
		require.NotEmpty(t, m[1])
	}
	re := regexp.MustCompile(pattern)
	match := re.FindStringSubmatch("2.5hrs")
	require.NotNil(t, match)
	require.Contains(t, match[0], "2.5")
}

func TestMinsRegex(t *testing.T) {
	pattern := `^(?P<mins>(\d+(\.\d+)?))\s*(m|min|mins?|minute|minutes?)`
	for _, val := range []string{"9m", "9min", "9mins", "9minute", "9minutes"} {
		re := regexp.MustCompile(pattern)
		m := re.FindStringSubmatch(val)
		require.NotNil(t, m)
		require.NotEmpty(t, m[1])
	}
	re := regexp.MustCompile(pattern)
	match := re.FindStringSubmatch("0.5min")
	require.NotNil(t, match)
	require.Contains(t, match[0], "0.5")
}

func TestSecsRegex(t *testing.T) {
	pattern := `^(?P<secs>(\d+(\.\d+)?))\s*(s|sec|secs?|second|seconds?)`
	for _, val := range []string{"15s", "15sec", "15secs", "15second", "15seconds"} {
		re := regexp.MustCompile(pattern)
		m := re.FindStringSubmatch(val)
		require.NotNil(t, m)
		require.NotEmpty(t, m[1])
	}
	re := regexp.MustCompile(pattern)
	match := re.FindStringSubmatch("3.25s")
	require.NotNil(t, match)
	require.Contains(t, match[0], "3.25")
}

func TestMinclockRegex(t *testing.T) {
	pattern := `^(?P<mins>\d{1,2}):(?P<secs>\d{2}(\.\d*)?)$`
	re := regexp.MustCompile(pattern)
	m := re.FindStringSubmatch("3:09")
	require.NotNil(t, m)
	m2 := re.FindStringSubmatch("5:30.5")
	require.NotNil(t, m2)
}

func TestHourclockRegex(t *testing.T) {
	pattern := `^(?P<hours>\d+):(?P<mins>[0-5]?\d):(?P<secs>[0-5]?\d(\.\d*)?)$`
	re := regexp.MustCompile(pattern)
	m := re.FindStringSubmatch("10:23:59")
	require.NotNil(t, m)
	m2 := re.FindStringSubmatch("1:01:01.1")
	require.NotNil(t, m2)
}

func TestDayclockRegex(t *testing.T) {
	pattern := `^(?P<days>\d+):(?P<hours>[0-2]?\d):(?P<mins>[0-5]?\d):(?P<secs>[0-5]?\d(\.\d*)?)$`
	re := regexp.MustCompile(pattern)
	m := re.FindStringSubmatch("2:10:23:12")
	require.NotNil(t, m)
	m2 := re.FindStringSubmatch("2:10:23:12.249")
	require.NotNil(t, m2)
}