package public_tests

import (
	"testing"
)

type testPr struct{}

func (testPr) GetStartNode() interface{} { return "publicStart" }
func (testPr) GetExitNode() interface{}  { return "publicExit" }
func (testPr) GetPreds(interface{}) []interface{} { return []interface{}{"predX"} }
func (testPr) GetSuccs(interface{}) []interface{} { return []interface{}{"succY"} }
func (testPr) GetAllNodes() []interface{}         { return []interface{}{"publicStart", "publicExit"} }
func (testPr) GetOwner(interface{}) interface{}   { return "ownerZ" }

func TestProgramRepresentationDifferentNodes(t *testing.T) {
	pr := testPr{}
	if pr.GetStartNode() != "publicStart" {
		t.Error("start node mismatch")
	}
	if pr.GetExitNode() != "publicExit" {
		t.Error("exit node mismatch")
	}
	if pr.GetOwner("publicStart") != "ownerZ" {
		t.Error("owner mismatch")
	}
	itPred := pr.GetPreds("publicExit")
	if len(itPred) == 0 {
		t.Error("preds not returned")
	}
	itSucc := pr.GetSuccs("publicStart")
	if len(itSucc) == 0 {
		t.Error("succs not returned")
	}
}

type testPr2 struct{}

func (testPr2) GetStartNode() interface{} { return "begin" }
func (testPr2) GetExitNode() interface{}  { return "finish" }
func (testPr2) GetPreds(interface{}) []interface{} { return nil }
func (testPr2) GetSuccs(interface{}) []interface{} { return nil }
func (testPr2) GetAllNodes() []interface{}         { return nil }
func (testPr2) GetOwner(interface{}) interface{}   { return nil }

func TestNullIterables(t *testing.T) {
	pr := testPr2{}
	if pr.GetStartNode() != "begin" {
		t.Error("start node mismatch")
	}
	if pr.GetExitNode() != "finish" {
		t.Error("exit node mismatch")
	}
	if pr.GetOwner("whatever") != nil {
		t.Error("expected nil owner")
	}
}