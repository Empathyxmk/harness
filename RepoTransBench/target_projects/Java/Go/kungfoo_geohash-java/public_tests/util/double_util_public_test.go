package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/util"
)

func TestPositiveValue_public(t *testing.T) {
	assert.InEpsilon(t, 27.0, util.RemainderWithFix(27.0, 360), 0.00001)
	assert.InEpsilon(t, 199.5, util.RemainderWithFix(919.5, 360), 0.00001)
}

func TestNegativeValue_public(t *testing.T) {
	assert.InEpsilon(t, 320.2, util.RemainderWithFix(-39.8, 360), 0.00001)
	assert.InEpsilon(t, 111.1, util.RemainderWithFix(-248.9, 360), 0.00001)
}