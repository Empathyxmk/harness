package callgraph

import (
	"testing"
)

type PointsToAnalysis[K comparable, V comparable] struct{}

func NewPointsToAnalysis[K comparable, V comparable]() *PointsToAnalysis[K,V] {
	return &PointsToAnalysis[K,V]{}
}

func TestPointsToAnalysisCoverage(t *testing.T) {
	_ = NewPointsToAnalysis[string, string]()
}