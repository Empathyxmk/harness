package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type NexmarkTableSourceFactory struct{}
type NexmarkTableSource struct {
	Config string // Simplified placeholder
}
type GeneratorConfig struct{}
type NexmarkConfiguration struct{}

func getAllOptions() map[string]string {
	return map[string]string{
		"connector": "nexmark",
	}
}

func createTableSource(options map[string]string) NexmarkTableSource {
	// This is a stand-in for a real factory implementation.
	return NexmarkTableSource{Config: options["connector"]}
}

func TestCommonProperties(t *testing.T) {
	properties := getAllOptions()
	actualSource := createTableSource(properties)
	expectedSource := NexmarkTableSource{Config: "nexmark"}
	assert.Equal(t, expectedSource, actualSource)
}

func TestCustomProperties(t *testing.T) {
	properties := getAllOptions()
	properties["rate.shape"] = "SQUARE"
	properties["rate.period"] = "11 min"
	properties["rate.limited"] = "true"
	properties["first-event.rate"] = "99"
	properties["next-event.rate"] = "199"
	properties["person.avg-size"] = "1kb"
	properties["auction.avg-size"] = "5kb"
	properties["bid.avg-size"] = "8kb"
	properties["person.proportion"] = "30"
	properties["auction.proportion"] = "15"
	properties["bid.proportion"] = "5"
	properties["bid.hot-ratio.auctions"] = "3"
	properties["bid.hot-ratio.bidders"] = "5"
	properties["auction.hot-ratio.sellers"] = "8"
	properties["events.num"] = "100"

	actualSource := createTableSource(properties)
	expectedSource := NexmarkTableSource{Config: "nexmark"}
	assert.Equal(t, expectedSource, actualSource)
}