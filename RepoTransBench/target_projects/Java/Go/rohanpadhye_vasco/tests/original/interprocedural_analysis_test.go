package original

import (
	"testing"
	"vasco"
)

type pr struct{}

func (pr) GetStartNode() interface{} { return "start" }
func (pr) GetExitNode() interface{}  { return "exit" }
func (pr) GetPreds(interface{}) []interface{} { return nil }
func (pr) GetSuccs(interface{}) []interface{} { return nil }
func (pr) GetAllNodes() []interface{}         { return nil }
func (pr) GetOwner(interface{}) interface{}   { return nil }

func TestTrivialAnalysis(t *testing.T) {
	dpr := pr{}
	_ = vasco.NewForwardInterProceduralAnalysis(dpr, nil)
}