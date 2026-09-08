package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/util"
)

func TestPositiveValue(t *testing.T) {
	assert.InEpsilon(t, 58.1541, util.RemainderWithFix(58.1541, 360), 0.00001)
	assert.InEpsilon(t, 93.1541, util.RemainderWithFix(453.1541, 360), 0.00001)
}

func TestNegativeValue(t *testing.T) {
	assert.InEpsilon(t, 301.8459, util.RemainderWithFix(-58.1541, 360), 0.00001)
	assert.InEpsilon(t, 266.8459, util.RemainderWithFix(-453.1541, 360), 0.00001)
}