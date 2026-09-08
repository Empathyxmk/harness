package public_tests

import (
	"testing"

	"racwn_wp_file_analyser/wpanalyser"
	"github.com/stretchr/testify/assert"
)

func TestPublicAnalyserBranches_BranchScenarioA(t *testing.T) {
	input := "branches_A"
	expected := "expected_output_A"
	actual := wpanalyser.AnalyseBranches(input)
	assert.Equal(t, expected, actual, "Branch scenario A should match expected output")
}

func TestPublicAnalyserBranches_BranchScenarioB(t *testing.T) {
	input := "branches_B"
	expected := "expected_output_B"
	actual := wpanalyser.AnalyseBranches(input)
	assert.Equal(t, expected, actual, "Branch scenario B should match expected output")
}