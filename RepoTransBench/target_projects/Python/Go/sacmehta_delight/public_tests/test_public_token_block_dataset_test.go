package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type TokenBlockDataset struct {
	tokens    []int
	blockSize int
}

func NewTokenBlockDataset(data []int, blockSize int) *TokenBlockDataset {
	return &TokenBlockDataset{
		tokens:    data,
		blockSize: blockSize,
	}
}

func (tb *TokenBlockDataset) NumBlocks() int {
	if tb.blockSize == 0 {
		return 0
	}
	return len(tb.tokens) / tb.blockSize
}

func (tb *TokenBlockDataset) Block(i int) []int {
	start := i * tb.blockSize
	end := start + tb.blockSize
	if end > len(tb.tokens) {
		end = len(tb.tokens)
	}
	return tb.tokens[start:end]
}

func TestTokenBlockDatasetPublicProperties(t *testing.T) {
	tokens := []int{5, 3, 7, 8, 1, 4, 9, 2, 6, 0}
	blockSize := 4
	ds := NewTokenBlockDataset(tokens, blockSize)
	assert.Equal(t, 2, ds.NumBlocks())
	block := ds.Block(1)
	assert.Equal(t, []int{8, 1, 4, 9}, block)
}

func TestTokenBlockDatasetPublicIter(t *testing.T) {
	tokens := []int{7, 3, 2, 1, 8, 6, 4, 5, 9, 0, 11, 13}
	blockSize := 6
	ds := NewTokenBlockDataset(tokens, blockSize)
	blocks := [][]int{}
	for i := 0; i < ds.NumBlocks(); i++ {
		blocks = append(blocks, ds.Block(i))
	}
	assert.Equal(t, 2, len(blocks))
	assert.True(t, blocks[0][len(blocks[0])-1] == tokens[5] || blocks[1][len(blocks[1])-1] == tokens[11])
}