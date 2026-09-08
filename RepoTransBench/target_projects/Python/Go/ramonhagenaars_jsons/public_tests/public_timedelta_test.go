package public_tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestTimedeltaDumpPublic(t *testing.T) {
	td := 2*24*time.Hour + 5*time.Hour
	dumped := jsons.DumpTimedelta(td)
	assert.Equal(t, 190800.0, dumped)
}

func TestTimedeltaLoadPublic(t *testing.T) {
	loaded := jsons.LoadTimedelta(3600.0)
	assert.Equal(t, time.Hour, loaded)
}