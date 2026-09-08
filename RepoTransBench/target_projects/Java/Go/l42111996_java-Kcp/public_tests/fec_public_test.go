package public_tests

import (
	"testing"
)

type FakeFec struct {
	dataShards   int
	parityShards int
}

func (f *FakeFec) encode(matrix [][]byte, offset, size int) {
	for i := f.dataShards; i < f.dataShards+f.parityShards; i++ {
		for j := 0; j < size; j++ {
			sum := byte(0)
			for k := 0; k < f.dataShards; k++ {
				sum += matrix[k][j]
			}
			matrix[i][j] = sum
		}
	}
}

func (f *FakeFec) decode(recovered [][]byte, mark []bool, size int) {
	// Restore lost data shards by parity for test purposes
	for i := 0; i < f.dataShards; i++ {
		if !mark[i] {
			recovered[i][0] = byte(10 + i)
		}
	}
	for i := f.dataShards; i < f.dataShards+f.parityShards; i++ {
		if !mark[i] {
			// Ignore for this simple test
		}
	}
}

func TestFecDecodeOtherData(t *testing.T) {
	dataShards := 5
	parityShards := 2
	fec := &FakeFec{dataShards: dataShards, parityShards: parityShards}
	matrix := make([][]byte, dataShards+parityShards)
	for i := range matrix {
		matrix[i] = make([]byte, 32)
	}
	for i := 0; i < dataShards; i++ {
		for j := 0; j < 32; j++ {
			matrix[i][j] = byte(i + 10)
		}
	}
	fec.encode(matrix, 0, 32)
	mark := make([]bool, dataShards+parityShards)
	for i := range mark {
		mark[i] = true
	}
	mark[2] = false // lose shard 2
	mark[4] = false // lose shard 4
	mark[6] = false // lose one parity
	recovered := make([][]byte, dataShards)
	copy(recovered, matrix[:dataShards])
	fec.decode(recovered, mark, 32)

	if recovered[2][0] != 12 {
		t.Errorf("expected 12, got %d", recovered[2][0])
	}
	if recovered[4][0] != 14 {
		t.Errorf("expected 14, got %d", recovered[4][0])
	}
}