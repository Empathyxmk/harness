package demo_scheduler

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestPublicScheduleAddition(t *testing.T) {
	start := time.Date(2025, 7, 1, 10, 0, 0, 0, time.UTC)
	delta := 20 * time.Second
	nextTime := func(start time.Time, delta time.Duration, count int) []time.Time {
		times := make([]time.Time, 0, count)
		t1 := start
		for i := 0; i < count; i++ {
			t1 = t1.Add(delta)
			times = append(times, t1)
		}
		return times
	}
	times := nextTime(start, delta, 2)
	assert.Equal(t, 2, len(times))
	assert.True(t, times[0].After(start))
	assert.Equal(t, 20.0, times[1].Sub(times[0]).Seconds())
}

func TestPublicScheduleTimesUnique(t *testing.T) {
	start := time.Date(2024, 12, 31, 23, 45, 0, 0, time.UTC)
	delta := 3 * time.Minute
	times := make([]time.Time, 0, 4)
	for i := 0; i < 4; i++ {
		times = append(times, start.Add(time.Duration(i)*delta))
	}
	// Use a map to check uniqueness
	unique := make(map[time.Time]struct{})
	for _, v := range times {
		unique[v] = struct{}{}
	}
	assert.Equal(t, 4, len(unique))
	assert.True(t, times[len(times)-1].After(start))
}