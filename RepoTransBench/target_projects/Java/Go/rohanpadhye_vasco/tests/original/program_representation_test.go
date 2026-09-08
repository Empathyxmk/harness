package original

import (
	"testing"
	"vasco"
)

type progRep struct{}

func (progRep) GetStartNode() interface{} { return "start" }
func (progRep) GetExitNode() interface{}  { return "exit" }
func (progRep) GetPreds(interface{}) []interface{} { return nil }
func (progRep) GetSuccs(interface{}) []interface{} { return nil }
func (progRep) GetAllNodes() []interface{}         { return nil }
func (progRep) GetOwner(interface{}) interface{}   { return nil }

func TestBasicOverride(t *testing.T) {
	pr := progRep{}
	if pr.GetStartNode() != "start" {
		t.Error("start node")
	}
	if pr.GetExitNode() != "exit" {
		t.Error("exit node")
	}
	if pr.GetPreds("x") != nil {
		t.Error("expected nil")
	}
}