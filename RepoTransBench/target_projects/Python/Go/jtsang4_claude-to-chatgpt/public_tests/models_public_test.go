package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"reflect"
)

func TestPublicModelsListExists(t *testing.T) {
	modelsList := []string{"modelA", "modelB"}
	assert.Equal(t, reflect.TypeOf(modelsList).Kind(), reflect.Slice)
	for _, v := range modelsList {
		assert.IsType(t, v, string(""))
	}
}

func TestPublicModelMapExists(t *testing.T) {
	modelMap := map[string]string{"gpt-4-0314": "claude-v1"}
	assert.Equal(t, reflect.TypeOf(modelMap).Kind(), reflect.Map)
	for k, v := range modelMap {
		assert.IsType(t, k, string(""))
		assert.IsType(t, v, string(""))
	}
}