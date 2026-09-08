package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/geohash"
)

func TestConstructorAndGetters(t *testing.T) {
	point := geohash.NewWGS84Point(10.0, 20.0)
	assert.InEpsilon(t, 10.0, point.Latitude(), 1e-10)
	assert.InEpsilon(t, 20.0, point.Longitude(), 1e-10)
}

func TestCopyConstructor(t *testing.T) {
	orig := geohash.NewWGS84Point(15.5, -30.2)
	copy := geohash.NewWGS84PointFromPoint(orig)
	assert.Equal(t, orig, copy)
	assert.Equal(t, orig.HashCode(), copy.HashCode())
}

func TestToString(t *testing.T) {
	point := geohash.NewWGS84Point(10.0, -45.7)
	assert.Equal(t, "(10.0,-45.7)", point.String())
}

func TestEqualsAndHashCode(t *testing.T) {
	p1 := geohash.NewWGS84Point(5, 6)
	p2 := geohash.NewWGS84Point(5, 6)
	p3 := geohash.NewWGS84Point(6, 5)
	assert.Equal(t, p1, p2)
	assert.Equal(t, p1.HashCode(), p2.HashCode())
	assert.NotEqual(t, p1, p3)
	assert.NotEqual(t, p2, nil)
	assert.NotEqual(t, p3, "not a point")
}

func TestOutOfRangeLatitude(t *testing.T) {
	assert.Panics(t, func() { geohash.NewWGS84Point(95.0, 20.0) })
	assert.Panics(t, func() { geohash.NewWGS84Point(-95.0, 20.0) })
}

func TestOutOfRangeLongitude(t *testing.T) {
	assert.Panics(t, func() { geohash.NewWGS84Point(10.0, 200.0) })
	assert.Panics(t, func() { geohash.NewWGS84Point(10.0, -200.0) })
}