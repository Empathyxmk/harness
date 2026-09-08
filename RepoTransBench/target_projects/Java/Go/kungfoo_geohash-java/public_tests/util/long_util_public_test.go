package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"kungfoo_geohash/util"
)

func TestCommonPrefixLength_public(t *testing.T) {
	assert.Equal(t, 64, util.CommonPrefixLength(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF))
	assert.Equal(t, 1, util.CommonPrefixLength(0x4000000000000000, 0xC000000000000000))
	assert.Equal(t, 31, util.CommonPrefixLength(0x80000000FFFFFFFF, 0x800000007FFFFFFF))
}