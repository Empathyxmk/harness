package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/geohash"
)

func TestConstructorAndGetters_public(t *testing.T) {
	point := geohash.NewWGS84Point(-35.4, 75.2)
	assert.InEpsilon(t, -35.4, point.Latitude(), 1e-10)
	assert.InEpsilon(t, 75.2, point.Longitude(), 1e-10)
}

func TestCopyConstructor_public(t *testing.T) {
	orig := geohash.NewWGS84Point(-60.5, 128.3)
	copy := geohash.NewWGS84PointFromPoint(orig)
	assert.Equal(t, orig, copy)
	assert.Equal(t, orig.HashCode(), copy.HashCode())
}

func TestToString_public(t *testing.T) {
	point := geohash.NewWGS84Point(-13.2, 102.8)
	assert.Equal(t, "(-13.2,102.8)", point.String())
}

func TestEqualsAndHashCode_public(t *testing.T) {
	p1 := geohash.NewWGS84Point(-90, 180)
	p2 := geohash.NewWGS84Point(-90, 180)
	p3 := geohash.NewWGS84Point(89.9, -179.9)
	assert.Equal(t, p1, p2)
	assert.Equal(t, p1.HashCode(), p2.HashCode())
	assert.NotEqual(t, p1, p3)
	assert.NotEqual(t, p2, nil)
	assert.NotEqual(t, p3, "some string")
}

func TestOutOfRangeLatitude_public(t *testing.T) {
	assert.Panics(t, func() {
		_ = geohash.NewWGS84Point(91.0, 10.0)
	})
	assert.Panics(t, func() {
		_ = geohash.NewWGS84Point(-91.0, 10.0)
	})
}

func TestOutOfRangeLongitude_public(t *testing.T) {
	assert.Panics(t, func() {
		_ = geohash.NewWGS84Point(0.0, 181.0)
	})
	assert.Panics(t, func() {
		_ = geohash.NewWGS84Point(0.0, -181.0)
	})
}