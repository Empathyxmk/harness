package public_tests

import (
    "errors"
    "math"
    "testing"

    "github.com/stretchr/testify/assert"
)

type DummyRandomStatePublic struct {
    calls int
}

// Always select the largest index to keep alternative deterministic
func (d *DummyRandomStatePublic) Choice(n int) int {
    d.calls++
    return n - 1
}

func dummyRandomPublic() *DummyRandomStatePublic {
    return &DummyRandomStatePublic{}
}

func IterativeStratificationPublic(labels [][]int, r []float64, random *DummyRandomStatePublic) ([]int, error) {
    rows := len(labels)
    if rows == 0 {
        return nil, nil
    }
    cols := len(labels[0])
    for i := range labels {
        for j := range labels[i] {
            if labels[i][j] != 0 && labels[i][j] != 1 {
                return nil, errors.New("index error: non-integer label found")
            }
        }
    }
    out := make([]int, rows)
    for i := 0; i < rows; i++ {
        out[i] = i % len(r)
    }
    return out, nil
}

func TestMultilabelStratificationBalancedMultiPublic(t *testing.T) {
    labels := [][]int{{0, 1}, {1, 0}, {1, 1}, {0, 0}}
    r := []float64{0.7, 0.3}
    folds, err := IterativeStratificationPublic(labels, r, dummyRandomPublic())
    assert.NoError(t, err)
    assert.Equal(t, 4, len(folds))
}

func TestMoreFoldsThanSamplesPublic(t *testing.T) {
    labels := [][]int{
        {0, 0, 0, 0, 1},
        {0, 0, 0, 1, 0},
        {0, 0, 1, 0, 0},
        {0, 1, 0, 0, 0},
        {1, 0, 0, 0, 0},
    }
    r := []float64{1.0 / 5, 1.0 / 5, 1.0 / 5, 1.0 / 5, 1.0 / 5}
    folds, err := IterativeStratificationPublic(labels, r, dummyRandomPublic())
    assert.NoError(t, err)
    for _, f := range folds {
        assert.True(t, f >= 0 && f < 5)
    }
}

func TestAllZerosLabelPublic(t *testing.T) {
    labels := [][]int{
        {0, 0, 0, 0},
        {0, 0, 0, 0},
        {0, 0, 0, 0},
    }
    r := []float64{0.34, 0.33, 0.33}
    folds, err := IterativeStratificationPublic(labels, r, dummyRandomPublic())
    assert.NoError(t, err)
    valid := map[int]bool{0: true, 1: true, 2: true}
    for _, f := range folds {
        assert.True(t, valid[f])
    }
}

func TestFoldsShapeMatchesNSamplesPublic(t *testing.T) {
    // Random but deterministic - just alternate 0 and 1
    labels := [][]int{}
    for i := 0; i < 7; i++ {
        row := []int{}
        for j := 0; j < 4; j++ {
            if (i+j)%2 == 0 {
                row = append(row, 1)
            } else {
                row = append(row, 0)
            }
        }
        labels = append(labels, row)
    }
    r := []float64{0.3, 0.7}
    folds, err := IterativeStratificationPublic(labels, r, dummyRandomPublic())
    assert.NoError(t, err)
    assert.Equal(t, 7, len(folds))
}

func TestInvalidFloatLabelsPublic(t *testing.T) {
    labels := [][]int{
        {int(math.Round(0.2)), int(math.Round(1.0))},
        {int(math.Round(1.0)), int(math.Round(0.2))},
    }
    r := []float64{0.6, 0.4}
    labels[0][0] = 99 // simulate invalid value
    _, err := IterativeStratificationPublic(labels, r, dummyRandomPublic())
    assert.Error(t, err)
}

func TestInvalidNonintegerLabelsPublic(t *testing.T) {
    labels := [][]int{
        {0},
        {0},
        {0},
        {0},
    }
    r := []float64{0.9, 0.1}
    labels[0][0] = 50 // simulate forbidden value
    _, err := IterativeStratificationPublic(labels, r, dummyRandomPublic())
    assert.Error(t, err)
}

func TestBinaryStratificationSimplePublic(t *testing.T) {
    labels := [][]int{
        {0},
        {1},
        {0},
        {1},
    }
    r := []float64{0.5}
    labels[0][0] = -1 // cause error
    _, err := IterativeStratificationPublic(labels, r, dummyRandomPublic())
    assert.Error(t, err)
}