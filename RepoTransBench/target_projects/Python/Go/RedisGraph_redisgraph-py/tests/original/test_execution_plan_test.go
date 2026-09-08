package original

import (
	"errors"
	"fmt"
	"testing"

	"redisgraph/execution_plan"

	"github.com/stretchr/testify/assert"
)

func TestProfileStatsFields(t *testing.T) {
	ps := execution_plan.NewProfileStats(10, 1.23)
	assert.Equal(t, 10, ps.RecordsProduced)
	assert.Equal(t, 1.23, ps.ExecutionTime)
}

func TestOperationEqAndStr(t *testing.T) {
	op1 := execution_plan.NewOperation("Filter", nil)
	op2 := execution_plan.NewOperation("Filter", nil)
	op3 := execution_plan.NewOperation("Scan", nil)
	op4 := execution_plan.NewOperation("Filter", execution_plan.WithArgs("x > 1"))

	assert.Equal(t, op1, op2)
	assert.NotEqual(t, op1, op3)
	assert.NotEqual(t, op1, op4)
	assert.Equal(t, "Filter", op1.String())
	assert.Equal(t, "Filter | x > 1", op4.String())
}

func TestOperationAppendAndChildCount(t *testing.T) {
	op := execution_plan.NewOperation("Root", nil)
	child := execution_plan.NewOperation("Child", nil)
	op.AppendChild(child)
	assert.Equal(t, 1, op.ChildCount())
	assert.Equal(t, child, op.Children[0])

	assert.Panics(t, func() {
		op.AppendChild(op)
	})
	assert.Panics(t, func() {
		op.AppendChild("not_op")
	})
}

type DummyEP struct {
	execution_plan.ExecutionPlan
}

func (d *DummyEP) OperationTree() *execution_plan.Operation {
	op1 := execution_plan.NewOperation("Root", nil)
	op2 := execution_plan.NewOperation("Child", nil)
	op1.AppendChild(op2)
	return op1
}

type OtherEP struct {
	execution_plan.ExecutionPlan
}

func (o *OtherEP) OperationTree() *execution_plan.Operation {
	return execution_plan.NewOperation("DifferentRoot", nil)
}

func TestExecutionPlanEqAndStrPatchTree(t *testing.T) {
	ep1 := &DummyEP{}
	ep2 := &DummyEP{}
	assert.Equal(t, ep1, ep2)
	assert.IsType(t, "", ep1.String())

	ep3 := &OtherEP{}
	assert.NotEqual(t, ep1, ep3)
}

func TestExecutionPlanInvalidInit(t *testing.T) {
	assert.Panics(t, func() {
		execution_plan.NewExecutionPlan("notalist")
	})
}

type ManualTreeEP struct {
	execution_plan.ExecutionPlan
}

func (d *ManualTreeEP) OperationTree() *execution_plan.Operation {
	op := execution_plan.NewOperation("A", nil)
	opB := execution_plan.NewOperation("B", nil)
	opC := execution_plan.NewOperation("C", nil)
	op.AppendChild(opB)
	op.AppendChild(opC)
	return op
}

func TestOperationTraverseManualTree(t *testing.T) {
	ep := &ManualTreeEP{}
	result := ep.OperationTraverse(ep.OperationTree(),
		func(x *execution_plan.Operation) string { return x.Name },
		func(c []string) string { return fmt.Sprintf("%v", c) },
		func(x, y string) string { return fmt.Sprintf("%s>%s", x, y) },
	)
	assert.Contains(t, result, "A>B")
}

func TestOperationTreeSimple(t *testing.T) {
	testCases := []struct {
		plan         []string
		expectedName string
	}{
		{
			[]string{
				"Project",
				"    Filter  (predicate: (n.v > 1))",
				"        NodeByLabelScan | (n:V)",
			},
			"Project",
		},
		{
			[]string{
				"Filter",
				"    NodeByLabelScan | (n:V)",
			},
			"Filter",
		},
	}
	for _, tc := range testCases {
		ep := execution_plan.NewExecutionPlan(tc.plan)
		assert.Equal(t, tc.expectedName, ep.OperationTree().Name)
	}
}