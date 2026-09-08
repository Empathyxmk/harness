package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/util"
)

func TestWidthHeight_public(t *testing.T) {
	assert.InEpsilon(t, 125.0, util.WidthDegreesForPrecision(1), 0.001)
	assert.InEpsilon(t, 5.0, util.WidthDegreesForPrecision(3), 0.001)
	assert.InEpsilon(t, 0.019, util.WidthDegreesForPrecision(7), 0.001)
	assert.InEpsilon(t, 625.0, util.HeightDegreesForPrecision(1), 0.001)
	assert.InEpsilon(t, 0.019, util.HeightDegreesForPrecision(7), 0.001)
}

func TestMaxPrecisionAndZero_public(t *testing.T) {
	assert.InEpsilon(t, 0.0006, util.WidthDegreesForPrecision(12), 0.0001)
	assert.InEpsilon(t, 0.0006, util.HeightDegreesForPrecision(12), 0.0001)
	assert.InEpsilon(t, 360.0, util.WidthDegreesForPrecision(0), 0.001)
	assert.InEpsilon(t, 180.0, util.HeightDegreesForPrecision(0), 0.001)
}