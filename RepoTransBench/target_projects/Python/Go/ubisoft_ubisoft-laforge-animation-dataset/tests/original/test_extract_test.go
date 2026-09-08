package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"lafan1/extract"
)

func TestPadAndConcatBasic(t *testing.T) {
	arrs := [][]float64{
		{0, 0},
		{0, 0},
		{1, 1},
		{1, 1},
	}
	reshaped := [][]float64{arrs[0:2], arrs[2:4]}
	result := extract.PadAndConcat(reshaped, 0)
	require.Equal(t, 4, len(result))
	require.Equal(t, 2, len(result[0]))
	isZero := true
	for i := 0; i < 2; i++ {
		for _, v := range result[i] {
			if v != 0 {
				isZero = false
				break
			}
		}
	}
	isOne := true
	for i := 2; i < 4; i++ {
		for _, v := range result[i] {
			if v != 1 {
				isOne = false
				break
			}
		}
	}
	require.True(t, isZero)
	require.True(t, isOne)
}

func TestPadAndConcatDifferentShapes(t *testing.T) {
	arrs := [][]float64{
		{0, 0},
		{0, 0},
		{1, 1},
		{1, 1},
		{1, 1},
	}
	reshaped := [][]float64{arrs[0:2], arrs[2:5]}
	result := extract.PadAndConcat(reshaped, 0)
	require.Equal(t, 5, len(result))
	require.Equal(t, 2, len(result[0]))
}

func TestFlattenDict(t *testing.T) {
	d := map[string]int{"a": 1, "b": 2}
	keys, vals := extract.FlattenDict(d)
	assert.ElementsMatch(t, []string{"a", "b"}, keys)
	assert.ElementsMatch(t, []int{1, 2}, vals)
}

func TestShapeReturnsCorrect(t *testing.T) {
	arr := make([][][]float64, 2)
	for i := range arr {
		arr[i] = make([][]float64, 3)
		for j := range arr[i] {
			arr[i][j] = make([]float64, 4)
		}
	}
	s := extract.Shape(arr)
	assert.Equal(t, []int{2, 3, 4}, s)

	arr2 := make([][]int, 2)
	for i := range arr2 {
		arr2[i] = make([]int, 3)
	}
	s2 := extract.Shape(arr2)
	assert.Equal(t, []int{2, 3}, s2)
}

func TestShapeEmpty(t *testing.T) {
	arr := make([][][]float64, 0)
	assert.Equal(t, []int{0}, extract.Shape(arr))
}

func TestParseBvhHierarchyAndMotion(t *testing.T) {
	text := `
HIERARCHY
ROOT Hips
{
    OFFSET 0.00 0.00 0.00
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Knee
    {
        OFFSET 0.00 1.00 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
    }
}
MOTION
Frames: 2
Frame Time: 0.0333333
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
1.0 1.0 1.0 0.5 0.5 0.5 0.1 0.2 0.3
`
	parsed, err := extract.ParseBvh(splitLines(text))
	require.NoError(t, err)
	_, ok1 := parsed["hierarchy"]
	_, ok2 := parsed["motion"]
	_, ok3 := parsed["channels"]
	assert.True(t, ok1 && ok2 && ok3)
	if m, ok := parsed["motion"].([][]float64); ok {
		assert.Equal(t, 2, len(m))
	} else {
		t.Errorf("motion not parsed as [][]float64")
	}
}

func TestParseBvhMalformed(t *testing.T) {
	_, err := extract.ParseBvh([]string{"nonsense", "not bvh"})
	assert.Error(t, err)
}

func splitLines(s string) []string {
	out := []string{}
	line := ""
	for i := 0; i < len(s); i++ {
		if s[i] == '\n' {
			out = append(out, line)
			line = ""
		} else {
			line += string(s[i])
		}
	}
	if len(line) > 0 {
		out = append(out, line)
	}
	return out
}