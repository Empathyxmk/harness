package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/util"
)

func TestCommonPrefixLength(t *testing.T) {
	assert.Equal(t, 64, util.CommonPrefixLength(0x123456789abcdef0, 0x123456789abcdef0))
	assert.Equal(t, 0, util.CommonPrefixLength(0x0000000000000000, 0x8000000000000000))
	assert.Equal(t, 63, util.CommonPrefixLength(0x8000000000000001, 0x8000000000000000))
	assert.Equal(t, 0, util.CommonPrefixLength(0x0, 0xFFFFFFFFFFFFFFFF))
}