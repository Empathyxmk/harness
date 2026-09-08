package original

import (
	"testing"

	"github.com/davidmoten/geo"
	"github.com/stretchr/testify/assert"
)

func TestDirectionOpposite(t *testing.T) {
	assert.Equal(t, geo.DirectionTop, geo.DirectionBottom.Opposite())
	assert.Equal(t, geo.DirectionBottom, geo.DirectionTop.Opposite())
	assert.Equal(t, geo.DirectionRight, geo.DirectionLeft.Opposite())
	assert.Equal(t, geo.DirectionLeft, geo.DirectionRight.Opposite())
}