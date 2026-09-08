package public_tests

import (
	"testing"

	"racwn_wp_file_analyser/wpanalyser"
	"github.com/stretchr/testify/assert"
)

func TestPublicAnalyserCore_CoreScenario1(t *testing.T) {
	input := "core_1"
	expected := "expected_core_1"
	actual := wpanalyser.AnalyseCore(input)
	assert.Equal(t, expected, actual, "Core scenario 1 output should match expected")
}

func TestPublicAnalyserCore_CoreScenario2(t *testing.T) {
	input := "core_2"
	expected := "expected_core_2"
	actual := wpanalyser.AnalyseCore(input)
	assert.Equal(t, expected, actual, "Core scenario 2 output should match expected")
}