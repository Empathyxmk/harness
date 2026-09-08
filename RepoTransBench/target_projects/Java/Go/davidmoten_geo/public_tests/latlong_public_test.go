package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/davidmoten/geo"
)

func TestLatLongPublicToStringDifferentValue(t *testing.T) {
	ll := geo.NewLatLong(-15.25, 35.75)
	assert.Equal(t, "LatLong [lat=-15.25, lon=35.75]", ll.String())
}

func TestLatLongHashCodeAndEqualsWithDifferentValues(t *testing.T) {
	lat := float32(-30.42)
	lon := float32(44.44)
	a := geo.NewLatLong(float64(lat), float64(lon))
	b := geo.NewLatLong(float64(lat), float64(lon))
	assert.Equal(t, a.HashCode(), b.HashCode())
	assert.Equal(t, a.Equals(b), true)
}