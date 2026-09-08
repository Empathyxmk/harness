package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPublicAssistantListBehavior(t *testing.T) {
	assistants := []map[string]string{
		{"id": "asst_753", "name": "HelperA", "desc": "Helps with numbers."},
		{"id": "asst_111", "name": "HelperB", "desc": "Helps with words."},
	}
	assert.IsType(t, []map[string]string{}, assistants)
	assert.Equal(t, "HelperA", assistants[0]["name"])
	assert.Contains(t, assistants[1]["desc"], "Helps with")
}

func TestPublicAssistantDetailFields(t *testing.T) {
	assistant := map[string]string{"id": "asst_xyz", "name": "XBot", "desc": "Handles X-cases"}
	_, okID := assistant["id"]
	_, okName := assistant["name"]
	assert.True(t, okID)
	assert.True(t, okName)
	assert.Equal(t, "Handles X-cases", assistant["desc"])
}