package public_tests

import (
	"testing"
	"vasco"
)

type pubPR struct{}
func (pubPR) GetStartNode() interface{} { return "alpha" }
func (pubPR) GetExitNode() interface{}  { return "omega" }
func (pubPR) GetPreds(interface{}) []interface{} { return []interface{}{} }
func (pubPR) GetSuccs(interface{}) []interface{} { return []interface{}{} }
func (pubPR) GetAllNodes() []interface{}         { return []interface{}{"alpha"} }
func (pubPR) GetOwner(interface{}) interface{}   { return "publicOwner" }

func TestDifferentConstructorPublic(t *testing.T) {
	pr := pubPR{}
	_ = vasco.NewOldForwardInterProceduralAnalysis(pr, nil)
}