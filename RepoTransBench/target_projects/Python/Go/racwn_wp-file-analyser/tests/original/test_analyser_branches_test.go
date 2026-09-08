package original

import (
	"testing"

	"racwn_wp_file_analyser/wpanalyser"
	"github.com/stretchr/testify/assert"
)

func TestAnalyserBranches_EdgeCase1(t *testing.T) {
	input := "edge_branch_1"
	expected := "expected_edge_1"
	actual := wpanalyser.AnalyseBranches(input)
	assert.Equal(t, expected, actual, "Should handle edge branch case 1 correctly")
}

func TestAnalyserBranches_EdgeCase2(t *testing.T) {
	input := "edge_branch_2"
	expected := "expected_edge_2"
	actual := wpanalyser.AnalyseBranches(input)
	assert.Equal(t, expected, actual, "Should handle edge branch case 2 correctly")
}