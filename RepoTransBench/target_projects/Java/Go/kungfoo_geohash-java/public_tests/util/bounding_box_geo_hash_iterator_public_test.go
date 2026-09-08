package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/geohash"
	"kungfoo_geohash/util"
)

func TestIterateBoundingBox_public(t *testing.T) {
	box := geohash.NewBoundingBox(10, 12, 33, 35)
	it := util.NewBoundingBoxGeoHashIterator(box, 6)
	hashes := make([]string, 0)
	for it.HasNext() {
		hashes = append(hashes, it.Next().ToBase32())
	}
	assert.NotEmpty(t, hashes)
	for _, hash := range hashes {
		assert.Equal(t, 6, len(hash))
	}
	unique := make(map[string]struct{})
	for _, h := range hashes {
		unique[h] = struct{}{}
	}
	assert.Equal(t, len(hashes), len(unique))
}

func TestSingleCellBoundingBox_public(t *testing.T) {
	verySmallBox := geohash.NewBoundingBox(0.01, 0.015, -0.02, -0.015)
	it := util.NewBoundingBoxGeoHashIterator(verySmallBox, 5)
	hashes := make([]string, 0)
	for it.HasNext() {
		hashes = append(hashes, it.Next().ToBase32())
	}
	assert.Equal(t, 1, len(hashes))
}