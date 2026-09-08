package original

import (
	"errors"
	"testing"

	"myusuf3_delorean/delorean"
	"github.com/stretchr/testify/assert"
)

func TestDeloreanErrorStrHtmlcov(t *testing.T) {
	e := delorean.NewDeloreanError("msg!")
	assert.Equal(t, "msg!", e.Error())
	assert.Implements(t, (*error)(nil), e)
}

func TestDeloreanInvalidTimezoneIsSubclassHtmlcov(t *testing.T) {
	e := delorean.NewDeloreanInvalidTimezone("bad tz")
	assert.Equal(t, "bad tz", e.Error())
	var derr *delorean.DeloreanError
	assert.True(t, errors.As(e, &derr))
}

func TestDeloreanInvalidDatetimeIsSubclassHtmlcov(t *testing.T) {
	e := delorean.NewDeloreanInvalidDatetime("bad dt")
	assert.Equal(t, "bad dt", e.Error())
	var derr *delorean.DeloreanError
	assert.True(t, errors.As(e, &derr))
}