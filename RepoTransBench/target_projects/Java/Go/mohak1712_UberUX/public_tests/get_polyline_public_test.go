package public_tests

import (
	"testing"
	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
)

func TestDecodePolylineDifferentCoordsPublic(t *testing.T) {
	g := &tests.GetPolyline{}
	testPolyline := "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
	result := g.DecodePoly(testPolyline)
	assert.True(t, len(result) >= 2)
}