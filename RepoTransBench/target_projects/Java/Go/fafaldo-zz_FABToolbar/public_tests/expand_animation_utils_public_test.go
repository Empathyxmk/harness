package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func getWidthAfterCollapse(initialWidth, deltaWidth int) int {
	return initialWidth - deltaWidth
}
func getWidthAfterExpand(initialWidth, deltaWidth int) int {
	return initialWidth + deltaWidth
}

func TestGetWidthAfterCollapse_withOtherParams(t *testing.T) {
	initialWidth := 100
	deltaWidth := 25
	expected := 75
	result := getWidthAfterCollapse(initialWidth, deltaWidth)
	assert.Equal(t, expected, result, "getWidthAfterCollapse should subtract widths")
}

func TestGetWidthAfterExpand_withOtherParams(t *testing.T) {
	initialWidth := 150
	deltaWidth := 45
	expected := 195
	result := getWidthAfterExpand(initialWidth, deltaWidth)
	assert.Equal(t, expected, result, "getWidthAfterExpand should add widths")
}