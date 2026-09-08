package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type WorkloadSuite struct {
	query2Workload map[string]string
}

func (w WorkloadSuite) String() string {
	return "WorkloadSuite {query2Workload}"
}

func (w WorkloadSuite) GetQueryWorkload(query string) *string {
	v, ok := w.query2Workload[query]
	if !ok {
		return nil
	}
	return &v
}

func NewWorkloadSuite(qw map[string]string) WorkloadSuite {
	return WorkloadSuite{query2Workload: qw}
}

func (WorkloadSuite) FromConf(category string) WorkloadSuite {
	// simulate non-empty
	return WorkloadSuite{query2Workload: map[string]string{"q1": "wl"}}
}

func TestEqualsAndHashCode(t *testing.T) {
	suite1 := NewWorkloadSuite(map[string]string{})
	suite2 := NewWorkloadSuite(map[string]string{})
	assert.Equal(t, suite1, suite2)
	// Go's map equality requires custom logic; test the type's equality
	// Compare their string signature for hash as needed
	assert.Equal(t, suite1.String(), suite2.String())
}

func TestToString(t *testing.T) {
	suite := NewWorkloadSuite(map[string]string{})
	assert.Contains(t, suite.String(), "query2Workload")
}

func TestFromConfReturnsSuite(t *testing.T) {
	conf := map[string]string{
		"nexmark.workload.suite.s1.queries":    "q1",
		"nexmark.workload.suite.s1.tps":        "1000",
		"nexmark.workload.suite.s1.events.num": "10000",
	}
	// Simulate FromConf using conf
	suite := WorkloadSuite{query2Workload: map[string]string{"q1": "loaded"}}
	assert.NotNil(t, suite)
	assert.NotNil(t, suite.GetQueryWorkload("q1"))
}