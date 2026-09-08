package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tusanai/mv2d/tests"
)

var dataFiles = []string{"configs/mv2d/data/two_frames.py"}

func TestPublicDataConfigKeysAndTypes(t *testing.T) {
	for _, dataPath := range dataFiles {
		module, err := tests.LoadPythonModule(dataPath)
		assert.NoError(t, err)
		assert.NotNil(t, module)
		assert.Contains(t, module, "class_names")
		cnames := module["class_names"]
		switch cnamesTyped := cnames.(type) {
		case []interface{}:
			assert.NotEmpty(t, cnamesTyped)
		case []string:
			assert.NotEmpty(t, cnamesTyped)
		default:
			assert.Fail(t, "class_names is not list/tuple")
		}
		assert.Contains(t, module, "train_pipeline")
		assert.IsType(t, []interface{}{}, module["train_pipeline"])
		for _, x := range module["train_pipeline"].([]interface{}) {
			_, ok := x.(map[string]interface{})
			assert.True(t, ok)
		}
		assert.Contains(t, module, "test_pipeline")
		assert.IsType(t, []interface{}{}, module["test_pipeline"])
		assert.Contains(t, module, "data")
		data := module["data"].(map[string]interface{})
		_, ok1 := data["train"]
		_, ok2 := data["val"]
		assert.True(t, ok1)
		assert.True(t, ok2)
	}
}

func TestPublicPointCloudRangeVariety(t *testing.T) {
	for _, dataPath := range dataFiles {
		module, err := tests.LoadPythonModule(dataPath)
		assert.NoError(t, err)
		pcrRaw, ok := module["point_cloud_range"]
		assert.True(t, ok)
		switch pcr := pcrRaw.(type) {
		case []interface{}:
			hasNeg := false
			hasPos := false
			for _, v := range pcr {
				f := v.(float64)
				if f < 0 {
					hasNeg = true
				}
				if f > 0 {
					hasPos = true
				}
			}
			assert.True(t, hasNeg && hasPos)
		}
	}
}