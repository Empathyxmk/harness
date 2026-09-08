package original

import (
	"fmt"
	"testing"
)

type Event struct {
	ID int
}

type NexmarkGenerator struct {
	current int
	max     int
}

func NewNexmarkGenerator(max int) *NexmarkGenerator {
	return &NexmarkGenerator{current: 0, max: max}
}

func (g *NexmarkGenerator) HasNext() bool {
	return g.current < g.max
}
func (g *NexmarkGenerator) Next() Event {
	defer func() { g.current++ }()
	return Event{ID: g.current}
}

func TestGenerate(t *testing.T) {
	generator := NewNexmarkGenerator(100)
	count := 0
	for generator.HasNext() {
		event := generator.Next()
		count++
		fmt.Printf("%v\n", event)
	}
	fmt.Printf("Total event: %d\n", count)
}