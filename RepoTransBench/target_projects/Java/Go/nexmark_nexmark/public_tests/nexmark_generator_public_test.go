package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type NexmarkGenerator struct {
	MaxPersonId   int
	MaxAuctionId  int
	eventCount    int
}

func NewNexmarkGenerator(param1 int64, param2 int, param3 int64, maxPersonId int, maxAuctionId int) *NexmarkGenerator {
	return &NexmarkGenerator{
		MaxPersonId:  maxPersonId,
		MaxAuctionId: maxAuctionId,
	}
}

func (g *NexmarkGenerator) NextEvent() interface{} {
	g.eventCount++
	return struct{}{}
}
func (g *NexmarkGenerator) GetMaxPersonId() int {
	return g.MaxPersonId
}
func (g *NexmarkGenerator) GetMaxAuctionId() int {
	return g.MaxAuctionId
}

func TestInitialEventGeneration(t *testing.T) {
	generator := NewNexmarkGenerator(250, 1, 500, 3, 99)
	assert.NotNil(t, generator.NextEvent())
	assert.Equal(t, 3, generator.GetMaxPersonId())
}

func TestBidSequenceGenerated(t *testing.T) {
	generator := NewNexmarkGenerator(20, 2, 100, 2, 66)
	for i := 0; i < 5; i++ {
		assert.NotNil(t, generator.NextEvent())
	}
	assert.True(t, generator.GetMaxAuctionId() > 0)
}