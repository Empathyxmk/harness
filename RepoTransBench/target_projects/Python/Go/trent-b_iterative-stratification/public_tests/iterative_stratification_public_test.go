package public_tests

import (
    "errors"
    "testing"

    "github.com/stretchr/testify/assert"
)

type DummyRandomStatePublic2 struct {
    calls int
}

func (d *DummyRandomStatePublic2) Choice(n int) int {
    d.calls++
    return n - 1
}

func IterativeStratificationPublic2(labels [][]int, r []float64, random *DummyRandomStatePublic2) ([]int, error) {
    rows := len(labels)
    if rows == 0 {
        return nil, nil
    }
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

func TestIterativeStratificationVariedPublic(t *testing.T) {
    params := []struct {
        labels          [][]int
        r               []float64
        expectedNFolds  int
        xfail           bool
    }{
        {
            labels: [][]int{
                {0, 1, 0},
                {0, 0, 1},
                {1, 1, 0},
                {0, 1, 1},
                {1, 0, 1},
            },
            r:              []float64{0.7, 0.3},
            expectedNFolds: 2,
            xfail:          false,
        },
        {
            labels: [][]int{
                {0},
                {0},
                {1},
                {1},
            },
            r:              []float64{0.4, 0.6},
            expectedNFolds: 2,
            xfail:          true,
        },
    }
    for _, param := range params {
        rs := &DummyRandomStatePublic2{}
        if param.xfail {
            param.labels[0][0] = -1
        }
        out, err := IterativeStratificationPublic2(param.labels, param.r, rs)
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

func TestIterativeStratificationAllOnesLabelPublic(t *testing.T) {
    labels := [][]int{
        {1, 1, 1},
        {1, 1, 1},
        {1, 1, 1},
        {1, 1, 1},
    }
    r := []float64{0.2, 0.4, 0.4}
    out, err := IterativeStratificationPublic2(labels, r, &DummyRandomStatePublic2{})
    assert.NoError(t, err)
    assert.Equal(t, 4, len(out))
}

func TestIterativeStratificationSingleFoldPublic(t *testing.T) {
    labels := [][]int{
        {1, 0, 0, 0, 0},
        {0, 1, 0, 0, 0},
        {0, 0, 1, 0, 0},
        {0, 0, 0, 1, 0},
        {0, 0, 0, 0, 1},
    }
    r := []float64{1.0}
    out, err := IterativeStratificationPublic2(labels, r, &DummyRandomStatePublic2{})
    assert.NoError(t, err)
    for _, v := range out {
        assert.Equal(t, 0, v)
    }
}

func TestIterativeStratificationRandomOutputTypesPublic(t *testing.T) {
    labels := [][]int{{0, 1}, {1, 1}}
    r := []float64{0.7, 0.3}
    out, err := IterativeStratificationPublic2(labels, r, &DummyRandomStatePublic2{})
    assert.NoError(t, err)
}

func TestIterativeStratificationAllZeroLabelsBranchPublic(t *testing.T) {
    labels := [][]int{
        {0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0},
    }
    r := []float64{0.2, 0.2, 0.2, 0.2, 0.2}
    out, err := IterativeStratificationPublic2(labels, r, &DummyRandomStatePublic2{})
    assert.NoError(t, err)
    assert.Equal(t, 3, len(out))
    for _, v := range out {
        assert.True(t, v >= 0 && v < 5)
    }
}