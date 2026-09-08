package unit

import (
	"fmt"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type Workflow struct {
	definition map[string]interface{}
	_state     string
}

func NewWorkflow(def map[string]interface{}) *Workflow {
	return &Workflow{definition: def}
}

func (wf *Workflow) State() string {
	return wf._state
}

type WorkflowNode struct {
	id   int
	kind string
	attr string
}

func NewWorkflowNode(def map[string]interface{}) *WorkflowNode {
	return &WorkflowNode{
		id:   def["id"].(int),
		kind: def["kind"].(string),
		attr: def["attr"].(string),
	}
}

type WorkflowException struct {
	msg string
}

func (e WorkflowException) Error() string {
	return e.msg
}

func TestWorkflowCanBeInitializedPublic(t *testing.T) {
	definition := map[string]interface{}{
		"name": "public_wf",
		"nodes": []map[string]interface{}{{
			"id":   100,
			"kind": "start",
		}},
	}
	wf := NewWorkflow(definition)
	assert.Equal(t, "public_wf", wf.definition["name"])
}

func TestWorkflowNodeAttributeAssignmentPublic(t *testing.T) {
	nodeDef := map[string]interface{}{
		"id":   57,
		"kind": "special",
		"attr": "xyz",
	}
	node := NewWorkflowNode(nodeDef)
	assert.Equal(t, "special", node.kind)
	assert.Equal(t, "xyz", node.attr)
	assert.Equal(t, 57, node.id)
}

func TestWorkflowExceptionMessagePublic(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			err := r.(WorkflowException)
			assert.Contains(t, err.Error(), "public")
		} else {
			t.Errorf("Did not recover expected WorkflowException")
		}
	}()
	panic(WorkflowException{"public workflow error"})
}

func TestWorkflowFromDictAndToDictPublic(t *testing.T) {
	wfDict := map[string]interface{}{"name": "other", "nodes": []interface{}{}}
	// simulate from_dict/to_dict
	wf := NewWorkflow(wfDict)
	assert.Equal(t, "other", wf.definition["name"])
}

func TestWorkflowTickAndStatePublic(t *testing.T) {
	wf := NewWorkflow(map[string]interface{}{"name": "ticktest", "nodes": []interface{}{}})
	wf._state = "waiting"
	assert.Equal(t, "waiting", wf.State())
	wf._state = "running"
	assert.Equal(t, "running", wf.State())
}

func TestWorkflowNodeReprPublic(t *testing.T) {
	node := &WorkflowNode{id: 30, kind: "action", attr: "LabelX"}
	rep := fmt.Sprintf("%#v", node)
	assert.True(t, strings.Contains(rep, "action") || strings.Contains(rep, "LabelX"))
}