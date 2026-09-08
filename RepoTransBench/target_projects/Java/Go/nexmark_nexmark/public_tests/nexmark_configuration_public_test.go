package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type RateShapeType string
type RateUnitType string

const (
	SQUARE     RateShapeType = "SQUARE"
	PER_SECOND RateUnitType  = "PER_SECOND"
)

type NexmarkConfiguration struct {
	numEvents        int
	rateShape        RateShapeType
	firstEventRate   int
	rateUnit         RateUnitType
	ratePeriodSec    int
	personProportion int
	bidProportion    int
	avgPersonByteSize int
	numInFlightAuctions int
	numActivePeople int
}

func defaultNexmarkConfiguration() NexmarkConfiguration {
	return NexmarkConfiguration{
		numEvents:        0,
		rateShape:        SQUARE,
		firstEventRate:   10000,
		rateUnit:         PER_SECOND,
		ratePeriodSec:    600,
		personProportion: 1,
		bidProportion:    46,
		avgPersonByteSize: 200,
		numInFlightAuctions: 100,
		numActivePeople:  1000,
	}
}

func TestDefaultValuesAreNotAllCustom(t *testing.T) {
	config := defaultNexmarkConfiguration()
	assert.NotEqual(t, 1, config.numEvents)
	assert.Equal(t, SQUARE, config.rateShape)
	assert.NotEqual(t, 20000, config.firstEventRate)
	assert.Equal(t, PER_SECOND, config.rateUnit)
	assert.NotEqual(t, 1200, config.ratePeriodSec)
	assert.True(t, config.personProportion < config.bidProportion)
	assert.NotEqual(t, 300, config.avgPersonByteSize)
	assert.NotEqual(t, 999, config.numInFlightAuctions)
	assert.True(t, config.numActivePeople > 0)
}

func TestEqualsAndHashCodeDiffObject(t *testing.T) {
	c1 := defaultNexmarkConfiguration()
	c2 := defaultNexmarkConfiguration()
	c1.firstEventRate = 12345
	assert.NotEqual(t, c1, c2)
	c2.firstEventRate = 12345
	assert.Equal(t, c1, c2)
	assert.Equal(t, hashCode(c1), hashCode(c2))
}

func hashCode(cfg NexmarkConfiguration) int {
	return cfg.numEvents + cfg.firstEventRate + cfg.numActivePeople
}