package public_tests

import (
	"testing"

	"redisgraph/execution_plan"

	"github.com/stretchr/testify/assert"
)

func TestPublicProfileStatsReprAndEquality(t *testing.T) {
	stats1 := execution_plan.NewProfileStats(23, 11.7)
	stats2 := execution_plan.NewProfileStats(23, 11.7)
	stats3 := execution_plan.NewProfileStats(29, 13.2)
	assert.Equal(t, stats1, stats2)
	assert.NotEqual(t, stats1, stats3)
}

func TestPublicOperationHierarchy(t *testing.T) {
	op := execution_plan.NewOperation("OpA", execution_plan.WithArgs(map[string]interface{}{"cost": 2}))
	opChild := execution_plan.NewOperation("OpB", execution_plan.WithArgs(map[string]interface{}{"cost": 3}))
	op.AppendChild(opChild)
	assert.Equal(t, opChild, op.Children[0])
	dct := op.ToDict()
	assert.Equal(t, "OpA", dct["name"])
}

func TestPublicExecutionPlanRepr(t *testing.T) {
	stats := execution_plan.NewProfileStats(7, 1.9)
	op := execution_plan.NewOperation("Scan", nil)
	ep := execution_plan.NewExecutionPlanWithRoot(op, stats)
	s := ep.String()
	assert.Contains(t, s, "Scan")
	assert.Contains(t, s, "records=7")
}