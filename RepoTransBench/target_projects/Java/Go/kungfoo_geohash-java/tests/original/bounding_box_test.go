package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	// hypothetical import, replace as needed with real package location
	"kungfoo_geohash/geohash"
)

func TestBoundingBoxConstructCorners(t *testing.T) {
	sw := geohash.NewWGS84Point(-10, -20)
	ne := geohash.NewWGS84Point(10, 20)
	box := geohash.NewBoundingBoxFromPoints(sw, ne)
	assert.InEpsilon(t, -10, box.SouthWestCorner().Latitude(), 1e-10)
	assert.InEpsilon(t, -20, box.SouthWestCorner().Longitude(), 1e-10)
	assert.InEpsilon(t, 10, box.NorthEastCorner().Latitude(), 1e-10)
	assert.InEpsilon(t, 20, box.NorthEastCorner().Longitude(), 1e-10)
	assert.InEpsilon(t, -10, box.SouthLatitude(), 1e-10)
	assert.InEpsilon(t, 10, box.NorthLatitude(), 1e-10)
	assert.InEpsilon(t, -20, box.WestLongitude(), 1e-10)
	assert.InEpsilon(t, 20, box.EastLongitude(), 1e-10)
}

func TestLatitudeLongitudeSize(t *testing.T) {
	box := geohash.NewBoundingBox(-10, 10, -20, 20)
	assert.InEpsilon(t, 20, box.LatitudeSize(), 1e-10)
	assert.InEpsilon(t, 40, box.LongitudeSize(), 1e-10)
}

func TestLongitudeWrapAroundMeridian(t *testing.T) {
	box := geohash.NewBoundingBox(-10, 10, 170, -170)
	assert.True(t, box.LongitudeSize() > 0)
}

func TestLongitudeEdgeCaseFullGlobe(t *testing.T) {
	box := geohash.NewBoundingBox(-10, 10, -180, 180)
	assert.InEpsilon(t, 360.0, box.LongitudeSize(), 0.00001)
}

func TestEqualsAndHashCode(t *testing.T) {
	box1 := geohash.NewBoundingBox(0, 10, 0, 20)
	box2 := geohash.NewBoundingBox(0, 10, 0, 20)
	box3 := geohash.NewBoundingBox(1, 10, 0, 20)
	assert.Equal(t, box1, box2)
	assert.Equal(t, box1.HashCode(), box2.HashCode())
	assert.NotEqual(t, box1, box3)
	assert.NotEqual(t, box1, nil)
	assert.NotEqual(t, box1, "not a box")
}

func TestThrowsOnSouthGreaterThanNorth(t *testing.T) {
	assert.Panics(t, func() { geohash.NewBoundingBox(10, -10, 0, 0) })
}

func TestThrowsOnOutOfRange(t *testing.T) {
	assert.Panics(t, func() { geohash.NewBoundingBox(-100, 10, 0, 0) })
	assert.Panics(t, func() { geohash.NewBoundingBox(-10, 95, 0, 0) })
	assert.Panics(t, func() { geohash.NewBoundingBox(-10, 10, 0, 190) })
	assert.Panics(t, func() { geohash.NewBoundingBox(-10, 10, -190, 0) })
}