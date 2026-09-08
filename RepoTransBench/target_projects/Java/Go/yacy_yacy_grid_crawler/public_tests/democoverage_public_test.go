package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"yacy_grid_crawler/tests"
)

func TestDemoCoveragePublic_AddOne_Public(t *testing.T) {
	result := tests.DemoCoverageAddOne(42)
	assert.Equal(t, 43, result)
}

func TestDemoCoveragePublic_SubtractOne_Public(t *testing.T) {
	result := tests.DemoCoverageSubtractOne(12)
	assert.Equal(t, 11, result)
}

func TestDemoCoveragePublic_AddOneWithNegativeValue_Public(t *testing.T) {
	result := tests.DemoCoverageAddOne(-7)
	assert.Equal(t, -6, result)
}