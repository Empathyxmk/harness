package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/davidmoten/geo"
)

func TestDirectionOppositeDifferentOrder(t *testing.T) {
	assert.Equal(t, geo.DirectionLeft, geo.DirectionRight.Opposite())
	assert.Equal(t, geo.DirectionRight, geo.DirectionLeft.Opposite())
	assert.Equal(t, geo.DirectionBottom, geo.DirectionTop.Opposite())
	assert.Equal(t, geo.DirectionTop, geo.DirectionBottom.Opposite())
}