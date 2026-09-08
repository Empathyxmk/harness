package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func convertPaddingDirection(input [][]int, pad, leftToRight, rightToLeft bool) [][]int {
	// This is a dummy reimplementation per test needs (Python logic uses torch).
	out := make([][]int, len(input))
	for i := range input {
		out[i] = make([]int, len(input[i]))
		copy(out[i], input[i])
		if leftToRight {
			// Move pad left to right
			pads := 0
			for _, v := range input[i] {
				if v == pad {
					pads++
				} else {
					break
				}
			}
			rest := input[i][pads:]
			for j := 0; j < len(rest); j++ {
				out[i][j] = rest[j]
			}
			for j := len(rest); j < len(out[i]); j++ {
				out[i][j] = pad
			}
		} else if rightToLeft {
			// Move pad right to left
			pads := 0
			for j := len(input[i]) - 1; j >= 0; j-- {
				if input[i][j] == pad {
					pads++
				} else {
					break
				}
			}
			rest := input[i][:len(input[i])-pads]
			for j := 0; j < pads; j++ {
				out[i][j] = pad
			}
			for j := 0; j < len(rest); j++ {
				out[i][pads+j] = rest[j]
			}
		}
	}
	return out
}

func makePositions(input [][]int, pad int) [][]int {
	// Simple version for this test, assume non-pad tokens get 2+increase by 1
	out := make([][]int, len(input))
	for i := range input {
		out[i] = make([]int, len(input[i]))
		n := 0
		for j := range input[i] {
			if input[i][j] == pad {
				out[i][j] = pad
			} else {
				n++
				out[i][j] = n + 1
			}
		}
	}
	return out
}

func TestConvertPaddingDirection(t *testing.T) {
	pad := 1
	leftPad := [][]int{
		{2, 3, 4, 5, 6},
		{1, 7, 8, 9, 10},
		{1, 1, 1, 11, 12},
	}
	rightPad := [][]int{
		{2, 3, 4, 5, 6},
		{7, 8, 9, 10, 1},
		{11, 12, 1, 1, 1},
	}

	assert.Equal(t, rightPad, convertPaddingDirection(leftPad, pad, true, false))
	assert.Equal(t, leftPad, convertPaddingDirection(rightPad, pad, false, true))
}

func TestMakePositions(t *testing.T) {
	pad := 1
	leftPadInput := [][]int{
		{9, 9, 9, 9, 9},
		{1, 9, 9, 9, 9},
		{1, 1, 1, 9, 9},
	}
	leftPadOutput := [][]int{
		{2, 3, 4, 5, 6},
		{1, 2, 3, 4, 5},
		{1, 1, 1, 2, 3},
	}
	rightPadInput := [][]int{
		{9, 9, 9, 9, 9},
		{9, 9, 9, 9, 1},
		{9, 9, 1, 1, 1},
	}
	rightPadOutput := [][]int{
		{2, 3, 4, 5, 6},
		{2, 3, 4, 5, 1},
		{2, 3, 1, 1, 1},
	}

	assert.Equal(t, leftPadOutput, makePositions(leftPadInput, pad))
	assert.Equal(t, rightPadOutput, makePositions(rightPadInput, pad))
}