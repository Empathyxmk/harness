package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type RateShapeType string
type RateUnitType string

const (
	SQUARE    RateShapeType = "SQUARE"
	PER_SECOND RateUnitType = "PER_SECOND"
)

type NexmarkConfiguration struct {
	numEvents           int
	numEventGenerators  int
	rateShape           RateShapeType
	firstEventRate      int
	nextEventRate       int
	rateUnit            RateUnitType
	ratePeriodSec       int
	preloadSeconds      int
	streamTimeout       int
	isRateLimited       bool
	useWallclockEventTime bool
	personProportion    int
	auctionProportion   int
	bidProportion       int
	avgPersonByteSize   int
	avgAuctionByteSize  int
	avgBidByteSize      int
	hotAuctionRatio     int
	hotSellersRatio     int
	hotBiddersRatio     int
	windowSizeSec       int
	windowPeriodSec     int
	watermarkHoldbackSec int
	numInFlightAuctions int
	numActivePeople     int
}

func defaultNexmarkConfiguration() NexmarkConfiguration {
	return NexmarkConfiguration{
		numEvents:           0,
		numEventGenerators:  1,
		rateShape:           SQUARE,
		firstEventRate:      10000,
		nextEventRate:       10000,
		rateUnit:            PER_SECOND,
		ratePeriodSec:       600,
		preloadSeconds:      0,
		streamTimeout:       240,
		isRateLimited:       false,
		useWallclockEventTime: false,
		personProportion:    1,
		auctionProportion:   3,
		bidProportion:       46,
		avgPersonByteSize:   200,
		avgAuctionByteSize:  500,
		avgBidByteSize:      100,
		hotAuctionRatio:     2,
		hotSellersRatio:     4,
		hotBiddersRatio:     4,
		windowSizeSec:       10,
		windowPeriodSec:     5,
		watermarkHoldbackSec: 0,
		numInFlightAuctions: 100,
		numActivePeople:     1000,
	}
}

func TestDefaultValues(t *testing.T) {
	config := defaultNexmarkConfiguration()
	assert.Equal(t, 0, config.numEvents)
	assert.Equal(t, 1, config.numEventGenerators)
	assert.Equal(t, SQUARE, config.rateShape)
	assert.Equal(t, 10000, config.firstEventRate)
	assert.Equal(t, 10000, config.nextEventRate)
	assert.Equal(t, PER_SECOND, config.rateUnit)
	assert.Equal(t, 600, config.ratePeriodSec)
	assert.Equal(t, 0, config.preloadSeconds)
	assert.Equal(t, 240, config.streamTimeout)
	assert.False(t, config.isRateLimited)
	assert.False(t, config.useWallclockEventTime)
	assert.Equal(t, 1, config.personProportion)
	assert.Equal(t, 3, config.auctionProportion)
	assert.Equal(t, 46, config.bidProportion)
	assert.Equal(t, 200, config.avgPersonByteSize)
	assert.Equal(t, 500, config.avgAuctionByteSize)
	assert.Equal(t, 100, config.avgBidByteSize)
	assert.Equal(t, 2, config.hotAuctionRatio)
	assert.Equal(t, 4, config.hotSellersRatio)
	assert.Equal(t, 4, config.hotBiddersRatio)
	assert.Equal(t, 10, config.windowSizeSec)
	assert.Equal(t, 5, config.windowPeriodSec)
	assert.Equal(t, 0, config.watermarkHoldbackSec)
	assert.Equal(t, 100, config.numInFlightAuctions)
	assert.Equal(t, 1000, config.numActivePeople)
}

func TestEqualsAndHashCode(t *testing.T) {
	c1 := defaultNexmarkConfiguration()
	c2 := defaultNexmarkConfiguration()
	assert.Equal(t, c1, c2)
	assert.Equal(t, hashCode(c1), hashCode(c2))
	c2.numEvents = 100
	assert.NotEqual(t, c1, c2)
}

func hashCode(cfg NexmarkConfiguration) int {
	// Simple hash combining major fields for testing use only (unlike Java's .hashCode)
	return cfg.numEvents + cfg.firstEventRate + cfg.nextEventRate + cfg.numEventGenerators
}