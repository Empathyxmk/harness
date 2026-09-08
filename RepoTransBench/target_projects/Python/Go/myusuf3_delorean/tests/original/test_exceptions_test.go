package original

import (
	"errors"
	"testing"

	"myusuf3_delorean/delorean"
	"github.com/stretchr/testify/assert"
)

func TestDeloreanErrorStr(t *testing.T) {
	e := delorean.NewDeloreanError("msg!")
	assert.Equal(t, "msg!", e.Error())
}

func TestDeloreanInvalidTimezoneIsSubclass(t *testing.T) {
	e := delorean.NewDeloreanInvalidTimezone("bad tz")
	assert.Contains(t, e.Error(), "bad tz")
	var derr *delorean.DeloreanError
	assert.True(t, errors.As(e, &derr))
}

func TestDeloreanInvalidDatetimeIsSubclass(t *testing.T) {
	e := delorean.NewDeloreanInvalidDatetime("bad dt")
	assert.Contains(t, e.Error(), "bad dt")
	var derr *delorean.DeloreanError
	assert.True(t, errors.As(e, &derr))
}