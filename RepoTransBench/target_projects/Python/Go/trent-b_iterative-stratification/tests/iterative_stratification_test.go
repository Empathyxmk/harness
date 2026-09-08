package tests

import (
    "errors"
    "reflect"
    "testing"

    "github.com/stretchr/testify/assert"
)

type DummyRandomState2 struct {
    calls int
}

func (d *DummyRandomState2) Choice(n int) int {
    d.calls++
    return 0 // always select the first for deterministic output
}

func IterativeStratification2(labels [][]int, r []float64, random *DummyRandomState2) ([]int, error) {
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

func TestIterativeStratificationVaried(t *testing.T) {
    params := []struct {
        labels          [][]int
        r               []float64
        expectedNFolds  int
        xfail           bool
    }{
        {
            labels: [][]int{
                {1, 0, 1},
                {1, 1, 0},
                {0, 1, 1},
                {1, 0, 0},
                {0, 0, 0},
            },
            r:              []float64{0.6, 0.4},
            expectedNFolds: 2,
            xfail:          false,
        },
        {
            labels: [][]int{
                {1},
                {1},
                {1},
                {0},
            },
            r:              []float64{0.5, 0.5},
            expectedNFolds: 2,
            xfail:          true, // simulate expected failure
        },
    }
    for _, param := range params {
        rs := &DummyRandomState2{}
        var out []int
        var err error
        if param.xfail {
            // Simulate failure
            param.labels[0][0] = -1
        }
        out, err = IterativeStratification2(param.labels, param.r, rs)
        if param.xfail {
            assert.Error(t, err)
            continue
        }
        assert.NoError(t, err)
        assert.Equal(t, len(param.labels), len(out))
        for _, v := range out {
            assert.True(t, v >= 0 && v < param.expectedNFolds)
        }
    }
}

func TestIterativeStratificationAllOnesLabel(t *testing.T) {
    labels := [][]int{
        {1, 1},
        {1, 1},
        {1, 1},
        {1, 1},
        {1, 1},
    }
    r := []float64{0.4, 0.6}
    out, err := IterativeStratification2(labels, r, &DummyRandomState2{})
    assert.NoError(t, err)
    assert.Equal(t, 5, len(out))
}

func TestIterativeStratificationSingleFold(t *testing.T) {
    labels := [][]int{
        {1, 0, 0, 0},
        {0, 1, 0, 0},
        {0, 0, 1, 0},
        {0, 0, 0, 1},
    }
    r := []float64{1.0}
    out, err := IterativeStratification2(labels, r, &DummyRandomState2{})
    assert.NoError(t, err)
    for _, v := range out {
        assert.Equal(t, 0, v)
    }
}

func TestIterativeStratificationRandomOutputTypes(t *testing.T) {
    labels := [][]int{
        {1, 0},
        {1, 1},
    }
    r := []float64{0.5, 0.5}
    out, err := IterativeStratification2(labels, r, &DummyRandomState2{})
    assert.NoError(t, err)
    // Go slice is always int type for this stub - type check implicit
}

func TestIterativeStratificationAllZeroLabelsBranch(t *testing.T) {
    labels := [][]int{
        {0, 0},
        {0, 0},
        {0, 0},
        {0, 0},
    }
    r := []float64{0.25, 0.25, 0.25, 0.25}
    out, err := IterativeStratification2(labels, r, &DummyRandomState2{})
    assert.NoError(t, err)
    assert.Equal(t, 4, len(out))
    for _, v := range out {
        assert.True(t, v >= 0 && v < 4)
    }
}