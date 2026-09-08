package public_tests

import (
	"errors"
	"testing"

	"myusuf3_delorean/delorean"
	"github.com/stretchr/testify/assert"
)

func TestDeloreanErrorStrPublic(t *testing.T) {
	e := delorean.NewDeloreanError("public error!")
	assert.Equal(t, "public error!", e.Error())
}

func TestDeloreanInvalidTimezoneIsSubclassPublic(t *testing.T) {
	e := delorean.NewDeloreanInvalidTimezone("public bad tz")
	assert.Contains(t, e.Error(), "public bad tz")
	var derr *delorean.DeloreanError
	assert.True(t, errors.As(e, &derr))
}

func TestDeloreanInvalidDatetimeIsSubclassPublic(t *testing.T) {
	e := delorean.NewDeloreanInvalidDatetime("public bad dt")
	assert.Contains(t, e.Error(), "public bad dt")
	var derr *delorean.DeloreanError
	assert.True(t, errors.As(e, &derr))
}