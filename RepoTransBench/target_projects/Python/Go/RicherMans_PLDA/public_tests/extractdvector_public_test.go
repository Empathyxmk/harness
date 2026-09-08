package public_tests

import (
	"encoding/gob"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"richermans_plda/scoring"
)

func TestDummyExtractDVectorPublic(t *testing.T) {
	X := [][]float64{
		{5, 7},
		{9, 11},
	}
	got := scoring.DummyExtractDVector(X)
	want := []float64{7, 9}
	assert.InDeltaSlice(t, want, got, 1e-7, "expected %#v got %#v", want, got)
}

func TestMainUsagePublic(t *testing.T) {
	ret := scoring.ExtractDVectorMain([]string{"extractdvector.py"})
	assert.Equal(t, 1, ret)
}

func TestMainOKPublic(t *testing.T) {
	tmpdir := t.TempDir()
	outPath := filepath.Join(tmpdir, "public_out.pkl")
	ret := scoring.ExtractDVectorMain([]string{"extractdvector.py", "dummy_in", outPath})
	assert.Equal(t, 0, ret)
	// Read saved output and check array
	f, err := os.Open(outPath)
	if err != nil {
		t.Fatalf("failed to open output: %v", err)
	}
	defer f.Close()
	decoder := gob.NewDecoder(f)
	var arr []float64
	if err := decoder.Decode(&arr); err != nil {
		t.Fatalf("failed to decode array: %v", err)
	}
	want := []float64{2, 3}
	assert.InDeltaSlice(t, want, arr, 1e-7, "expected %#v got %#v", want, arr)
}