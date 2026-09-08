package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/geohash"
)

func TestBoundingBoxConstructCorners_public(t *testing.T) {
	sw := geohash.NewWGS84Point(-55, 110)
	ne := geohash.NewWGS84Point(-15, 150)
	box := geohash.NewBoundingBoxFromPoints(sw, ne)
	assert.InEpsilon(t, -55, box.SouthWestCorner().Latitude(), 1e-10)
	assert.InEpsilon(t, 110, box.SouthWestCorner().Longitude(), 1e-10)
	assert.InEpsilon(t, -15, box.NorthEastCorner().Latitude(), 1e-10)
	assert.InEpsilon(t, 150, box.NorthEastCorner().Longitude(), 1e-10)
	assert.InEpsilon(t, -55, box.SouthLatitude(), 1e-10)
	assert.InEpsilon(t, -15, box.NorthLatitude(), 1e-10)
	assert.InEpsilon(t, 110, box.WestLongitude(), 1e-10)
	assert.InEpsilon(t, 150, box.EastLongitude(), 1e-10)
}

func TestLatitudeLongitudeSize_public(t *testing.T) {
	box := geohash.NewBoundingBox(22, 44, -45, -33)
	assert.InEpsilon(t, 22.0, box.LatitudeSize(), 1e-10)
	assert.InEpsilon(t, 12.0, box.LongitudeSize(), 1e-10)
}

func TestLongitudeWrapAroundMeridian_public(t *testing.T) {
	box := geohash.NewBoundingBox(-40, 40, 179, -179)
	assert.True(t, box.LongitudeSize() > 0)
}

func TestLongitudeEdgeCaseFullGlobe_public(t *testing.T) {
	box := geohash.NewBoundingBox(0, 90, -180, 180)
	assert.InEpsilon(t, 360.0, box.LongitudeSize(), 0.00001)
}

func TestEqualsAndHashCode_public(t *testing.T) {
	b1 := geohash.NewBoundingBox(-10, 10, 50, 100)
	b2 := geohash.NewBoundingBox(-10, 10, 50, 100)
	b3 := geohash.NewBoundingBox(-11, 10, 50, 100)
	assert.Equal(t, b1, b2)
	assert.Equal(t, b1.HashCode(), b2.HashCode())
	assert.NotEqual(t, b1, b3)
	assert.NotEqual(t, b1, nil)
	assert.NotEqual(t, b1, "something else")
}

func TestThrowsOnSouthGreaterThanNorth_public(t *testing.T) {
	assert.Panics(t, func() {
		_ = geohash.NewBoundingBox(20, 10, 0, 0)
	})
}

func TestThrowsOnOutOfRange_public(t *testing.T) {
	assert.Panics(t, func() {
		_ = geohash.NewBoundingBox(-100, 10, 0, 0)
	})
	assert.Panics(t, func() {
		_ = geohash.NewBoundingBox(-10, 95.5, 0, 0)
	})
	assert.Panics(t, func() {
		_ = geohash.NewBoundingBox(-10, 10, 0, 200)
	})
	assert.Panics(t, func() {
		_ = geohash.NewBoundingBox(-10, 10, -200, 0)
	})
}