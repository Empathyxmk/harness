package original

import (
	"testing"
	"vasco"
)

type dummyBackwardPR struct{}

func (dummyBackwardPR) GetStartNode() interface{} { return "start" }
func (dummyBackwardPR) GetExitNode() interface{}  { return "exit" }
func (dummyBackwardPR) GetPreds(interface{}) []interface{} { return []interface{}{} }
func (dummyBackwardPR) GetSuccs(interface{}) []interface{} { return []interface{}{} }
func (dummyBackwardPR) GetAllNodes() []interface{}         { return []interface{}{"start"} }
func (dummyBackwardPR) GetOwner(interface{}) interface{}   { return "owner" }

func TestBackwardCoverageAbstract(t *testing.T) {
	pr := dummyBackwardPR{}
	_ = vasco.NewBackwardInterProceduralAnalysis(pr, nil)
}