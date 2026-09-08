package tests

import (
	"testing"

	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/stretchr/testify/assert"
)

func TestExtractOne(t *testing.T) {
	choices := []string{"new york jets", "new york giants", "liverpool"}
	query := "new york jets"
	result := fuzzywuzzy.ExtractOne(query, choices)
	match, _ := result.(fuzzywuzzy.MatchResult)
	assert.Equal(t, "new york jets", match.Value)
}

func TestExtractLimitAndProcessor(t *testing.T) {
	choices := []string{"foo Xbar", "bar", "baz"}
	query := "foo bar"
	results := fuzzywuzzy.Extract(query, choices, fuzzywuzzy.LowerProcessor, fuzzywuzzy.TokenSortRatio, 2)
	assert.Equal(t, 2, len(results))
}

func TestExtractNone(t *testing.T) {
	assert.Nil(t, fuzzywuzzy.ExtractOne(nil, nil))
	results := fuzzywuzzy.Extract(nil, nil, nil, nil, 0)
	assert.NotNil(t, results)
	assert.Equal(t, 0, len(results))
}

func TestEmptyChoicesExtractOne(t *testing.T) {
	assert.Nil(t, fuzzywuzzy.ExtractOne("a", []string{}))
	results := fuzzywuzzy.Extract("a", []string{}, nil, nil, 0)
	assert.NotNil(t, results)
	assert.Equal(t, 0, len(results))
}

func TestIndexedChoices(t *testing.T) {
	choices := map[string]string{"a": "foo", "b": "boo"}
	result := fuzzywuzzy.ExtractOneIndexed("foo", choices)
	match, _ := result.(fuzzywuzzy.MatchResult)
	assert.Equal(t, "foo", match.Value)
}