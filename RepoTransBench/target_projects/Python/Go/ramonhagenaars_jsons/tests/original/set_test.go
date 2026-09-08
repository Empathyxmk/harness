package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestDumpSet(t *testing.T) {
	d := time.Date(2018, 7, 8, 21, 34, 0, 0, time.UTC)
	set_ := map[time.Time]struct{}{d: {}, d: {}}
	dumped := jsons.DumpSet(set_)
	expected := []string{"2018-07-08T21:34:00Z"}
	assert.Equal(t, expected, dumped)
}

func TestLoadSet(t *testing.T) {
	d := time.Date(2018, 7, 8, 21, 34, 0, 0, time.UTC)
	loaded1 := jsons.LoadSet([]string{"2018-07-08T21:34:00Z"}, true)
	assert.Equal(t, map[time.Time]struct{}{d: {}}, loaded1)
	loaded2 := jsons.LoadSet([]string{"2018-07-08T21:34:00Z"}, false)
	assert.Equal(t, []string{"2018-07-08T21:34:00Z"}, loaded2)
}