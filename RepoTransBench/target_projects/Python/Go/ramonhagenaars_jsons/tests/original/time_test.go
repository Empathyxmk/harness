package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestDumpTime(t *testing.T) {
	d := time.Date(2018, 7, 8, 21, 34, 0, 0, time.UTC)
	dumped := jsons.DumpTime(d)
	assert.Equal(t, "21:34:00", dumped)
}

func TestLoadTime(t *testing.T) {
	expected := time.Date(2018, 7, 8, 21, 34, 0, 0, time.UTC)
	loaded := jsons.LoadTime("21:34:00")
	// time.Date and loaded must be same time, date is ignored for time of day
	assert.Equal(t, expected.Format("15:04:05"), loaded.Format("15:04:05"))
}