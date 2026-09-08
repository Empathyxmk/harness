package unit

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var VERSION = "0.8.0"

func TestVersionValuePublic(t *testing.T) {
	parts := strings.Split(VERSION, ".")
	assert.Equal(t, []string{"0", "8", "0"}, parts)
}

type Workflow struct{}
type WorkflowException struct{}
type WorkflowNode struct{}

func TestWorkflowsAllExportsPublic(t *testing.T) {
	w := Workflow{}
	wn := WorkflowNode{}
	we := WorkflowException{}
	assert.IsType(t, Workflow{}, w)
	assert.IsType(t, WorkflowNode{}, wn)
	assert.IsType(t, WorkflowException{}, we)
}

func TestExceptionIsExceptionPublic(t *testing.T) {
	type WorkflowException struct {
		msg string
	}
	defer func() {
		r := recover()
		if err, ok := r.(WorkflowException); ok {
			assert.Contains(t, err.msg, "different")
		} else {
			t.Errorf("Expected WorkflowException to be raised")
		}
	}()
	panic(WorkflowException{"different message"})
}