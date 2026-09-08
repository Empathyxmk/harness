package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/geohash"
	"kungfoo_geohash/util"
)

func TestXYGridSample_public(t *testing.T) {
	bbox := geohash.NewBoundingBox(1, 7, 20, 30)
	points := util.XYGridSample(bbox, 2, 3)
	assert.Equal(t, 6, len(points))
	for _, p := range points {
		assert.True(t, p.Latitude() >= 1 && p.Latitude() <= 7)
		assert.True(t, p.Longitude() >= 20 && p.Longitude() <= 30)
	}
}

func TestPointsSpread_public(t *testing.T) {
	bbox := geohash.NewBoundingBox(0, 1, 0, 2)
	points := util.XYGridSample(bbox, 2, 2)
	assert.Equal(t, 4, len(points))
	found := [4]bool{}
	for _, p := range points {
		if p.Latitude() == 0.0 && p.Longitude() == 0.0 {
			found[0] = true
		}
		if p.Latitude() == 0.0 && p.Longitude() == 2.0 {
			found[1] = true
		}
		if p.Latitude() == 1.0 && p.Longitude() == 0.0 {
			found[2] = true
		}
		if p.Latitude() == 1.0 && p.Longitude() == 2.0 {
			found[3] = true
		}
	}
	for _, f := range found {
		assert.True(t, f)
	}
}