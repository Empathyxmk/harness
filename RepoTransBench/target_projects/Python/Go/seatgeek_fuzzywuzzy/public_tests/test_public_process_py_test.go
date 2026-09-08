package public_tests

import (
	"testing"
	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/stretchr/testify/assert"
)

func TestExtractOnePublic(t *testing.T) {
	query := "python programmer"
	choices := []string{"java developer", "python engineer", "c++ guru"}
	match, score := fuzzywuzzy.ExtractOnePair(query, choices)
	assert.Contains(t, choices, match)
	assert.IsType(t, 0, score)
	assert.True(t, score > 0)
}

func TestExtractBestsPublic(t *testing.T) {
	query := "data science"
	choices := []string{"science data", "data analytics", "data scientist", "big data"}
	results := fuzzywuzzy.ExtractBests(query, choices, nil, nil, 2)
	assert.Equal(t, 2, len(results))
	for _, r := range results {
		match, score := r.Value, r.Score
		assert.Contains(t, choices, match)
		assert.IsType(t, 0, score)
		assert.True(t, score > 0)
	}
}