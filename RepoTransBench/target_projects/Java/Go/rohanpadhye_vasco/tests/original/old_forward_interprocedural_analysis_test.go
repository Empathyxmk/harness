package original

import (
	"testing"
	"vasco"
)

type dummyPR struct{}

func (dummyPR) GetStartNode() interface{} { return "start" }
func (dummyPR) GetExitNode() interface{}  { return "exit" }
func (dummyPR) GetPreds(interface{}) []interface{} { return []interface{}{} }
func (dummyPR) GetSuccs(interface{}) []interface{} { return []interface{}{} }
func (dummyPR) GetAllNodes() []interface{}         { return []interface{}{"start"} }
func (dummyPR) GetOwner(interface{}) interface{}   { return "owner" }

func TestBasicConstructor(t *testing.T) {
	pr := dummyPR{}
	_ = vasco.NewOldForwardInterProceduralAnalysis(pr, nil)
	// Just ensuring construction does not panic
}