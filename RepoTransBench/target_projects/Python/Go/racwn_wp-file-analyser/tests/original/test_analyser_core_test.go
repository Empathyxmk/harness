package original

import (
	"testing"

	"racwn_wp_file_analyser/wpanalyser"
	"github.com/stretchr/testify/assert"
)

func TestAnalyserCore_ErrorCase1(t *testing.T) {
	input := "error_core_1"
	expected := "expected_error_1"
	actual := wpanalyser.AnalyseCore(input)
	assert.Equal(t, expected, actual, "Should handle error core case 1 correctly")
}

func TestAnalyserCore_ErrorCase2(t *testing.T) {
	input := "error_core_2"
	expected := "expected_error_2"
	actual := wpanalyser.AnalyseCore(input)
	assert.Equal(t, expected, actual, "Should handle error core case 2 correctly")
}