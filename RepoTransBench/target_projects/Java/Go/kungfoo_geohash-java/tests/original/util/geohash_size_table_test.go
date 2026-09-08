package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/geohash"
	"kungfoo_geohash/util"
)

func TestNumberOfBitsForOverlappingGeoHashTypicalBox(t *testing.T) {
	box := geohash.NewBoundingBox(-1, 1, -1, 1)
	bits := util.NumberOfBitsForOverlappingGeoHash(box)
	assert.True(t, bits > 0 && bits <= 63)
}

func TestNumberOfBitsForTinyBoxHighPrecision(t *testing.T) {
	box := geohash.NewBoundingBox(0, 0.0001, 0, 0.0001)
	bits := util.NumberOfBitsForOverlappingGeoHash(box)
	assert.True(t, bits <= 63 && bits > 0)
}

func TestNumberOfBitsForHugeBoxLowPrecision(t *testing.T) {
	box := geohash.NewBoundingBox(-80, 80, -150, 150)
	bits := util.NumberOfBitsForOverlappingGeoHash(box)
	assert.True(t, bits < 63 && bits > 0)
}