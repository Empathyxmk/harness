package public_tests

import (
	"testing"
	"vasco"
)

type pubPr struct{}

func (pubPr) GetStartNode() interface{} { return "begin" }
func (pubPr) GetExitNode() interface{}  { return "end" }
func (pubPr) GetPreds(interface{}) []interface{} { return nil }
func (pubPr) GetSuccs(interface{}) []interface{} { return nil }
func (pubPr) GetAllNodes() []interface{}         { return nil }
func (pubPr) GetOwner(interface{}) interface{}   { return nil }

func TestTrivialAnalysisPublic(t *testing.T) {
	pr := pubPr{}
	_ = vasco.NewForwardInterProceduralAnalysis(pr, nil)
}