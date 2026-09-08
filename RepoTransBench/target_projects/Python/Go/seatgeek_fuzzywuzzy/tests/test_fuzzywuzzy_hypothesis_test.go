package tests

import (
	"testing"
	"unicode"
	"math/rand"
	"reflect"
	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/leanovate/gopter"
	"github.com/leanovate/gopter/prop"
)

// Simple property-based testing using gopter for string similarity
func scorerAndProcessorCases() []struct {
	Scorer    func(a, b string) int
	Processor func(string) string
} {
	return []struct {
		Scorer    func(a, b string) int
		Processor func(string) string
	}{
		{fuzzywuzzy.Ratio, func(x string) string { return x }},
		{fuzzywuzzy.PartialRatio, func(x string) string { return x }},
		{fuzzywuzzy.Ratio, func(x string) string { return fuzzywuzzy.FullProcess(x, false) }},
		{fuzzywuzzy.Ratio, func(x string) string { return fuzzywuzzy.FullProcess(x, true) }},
		// Add more as needed, following the pattern in the Python test.
	}
}

func TestIdenticalStringsExtracted(t *testing.T) {
	for _, pair := range scorerAndProcessorCases() {
		parameters := gopter.DefaultTestParameters()
		properties := gopter.NewProperties(parameters)
		properties.Property("identical strings have perfect match", prop.ForAll(
			func(strs []string) bool {
				if len(strs) == 0 {
					return true
				}
				idx := rand.Intn(len(strs))
				choice := strs[idx]
				if pair.Processor(choice) == "" {
					return true
				}
				results := fuzzywuzzy.ExtractBests(choice, strs, pair.Scorer, pair.Processor, 100)
				if len(results) == 0 {
					return false
				}
				found := false
				for _, r := range results {
					if reflect.DeepEqual(r, fuzzywuzzy.MatchResult{Value: choice, Score: 100}) {
						found = true
					}
				}
				return found
			},
			gopter.GenSliceOf(gopter.GenAnyString()),
		))
		properties.TestingRun(t)
	}
}

// Similarly, translate other property-based and parameterized tests as appropriate.