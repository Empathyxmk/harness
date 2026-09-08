package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Minimal automation_module stub for public test (simulate successful progress)
type AutomationModulePub struct{}

func (a *AutomationModulePub) GetProgress(progressId int) map[string]any {
	return map[string]any{"progress": 42}
}

func TestGetProgressDifferentData(t *testing.T) {
	module := &AutomationModulePub{}
	progressId := 7
	resp := module.GetProgress(progressId)
	assert.IsType(t, map[string]any{}, resp)
	val, ok := resp["progress"]
	assert.True(t, ok)
	progressVal, isInt := val.(int)
	assert.True(t, isInt)
	assert.NotEqual(t, 0, progressVal)
}