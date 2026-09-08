package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/davidmoten/geo"
)

func TestLatLongToString(t *testing.T) {
	ll := geo.NewLatLong(10, 20)
	assert.Equal(t, "LatLong [lat=10.0, lon=20.0]", ll.String())
}

func TestLatLongHashCode(t *testing.T) {
	lat, lon := float32(20.05), float32(-15.5)
	a := geo.NewLatLong(float64(lat), float64(lon))
	b := geo.NewLatLong(float64(lat), float64(lon))
	assert.Equal(t, a.HashCode(), b.HashCode())
	assert.Equal(t, a.Equals(b), true)
}