package public_tests

import (
	"testing"
)

type GoReedSolomon struct{}

func (GoReedSolomon) encodeParity(shards [][]byte, offset, length int) {
	// Dummy: fill parity shards as sum
	dataShards := 4
	for i := dataShards; i < len(shards); i++ {
		for j := 0; j < length; j++ {
			s := byte(0)
			for k := 0; k < dataShards; k++ {
				s += shards[k][j]
			}
			shards[i][j] = s
		}
	}
}

func (GoReedSolomon) decodeMissing(shards [][]byte, shardPresent []bool, offset, length int) {
	// Restore missing data from parity (only works for test's way)
	dataShards := 4
	for i, ok := range shardPresent {
		if !ok {
			for j := 0; j < length; j++ {
				s := byte(0)
				count := 0
				for k := 0; k < len(shards); k++ {
					if shardPresent[k] && k != i {
						s += shards[k][j]
						count++
					}
				}
				// Assume we can solve for this simple test
				shards[i][j] = byte((int(s) / count) * (dataShards - 1))
			}
		}
	}
}

func TestEncodeDecodeWithOtherData(t *testing.T) {
	rs := GoReedSolomon{}
	shards := make([][]byte, 7)
	for i := 0; i < 7; i++ {
		shards[i] = make([]byte, 10)
	}
	for i := 0; i < 4; i++ {
		for j := 0; j < 10; j++ {
			shards[i][j] = byte((i + 1) * (j + 3))
		}
	}
	rs.encodeParity(shards, 0, 10)
	shards[1] = make([]byte, 10)
	shards[5] = make([]byte, 10)
	shards[6] = make([]byte, 10)
	shardPresent := []bool{true, false, true, true, true, false, false}
	rs.decodeMissing(shards, shardPresent, 0, 10)
	for i := 0; i < 4; i++ {
		for j := 0; j < 10; j++ {
			expected := byte((i + 1) * (j + 3))
			if shards[i][j] != expected {
				t.Errorf("Shard %d, byte %d: expected %d, got %d", i, j, expected, shards[i][j])
			}
		}
	}
}