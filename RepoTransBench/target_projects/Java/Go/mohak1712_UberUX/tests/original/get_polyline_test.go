package original

import (
	"testing"

	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
)

func TestGetPolylineDecodePolyReturnsCorrectSize(t *testing.T) {
	poly := &tests.GetPolyline{}
	encoded := "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
	assert.Equal(t, 3, len(poly.DecodePoly(encoded)))
}

func TestGetPolylineDecodePolyEmptyString(t *testing.T) {
	poly := &tests.GetPolyline{}
	assert.Equal(t, 0, len(poly.DecodePoly("")))
}