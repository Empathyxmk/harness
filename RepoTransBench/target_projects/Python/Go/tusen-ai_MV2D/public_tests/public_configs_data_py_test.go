package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tusanai/mv2d/tests"
)

func TestPublicConfigsDataTwoFramesExecutable(t *testing.T) {
	path := "configs/mv2d/data/two_frames.py"
	module, err := tests.LoadPythonModule(path)
	assert.NoError(t, err)
	assert.NotNil(t, module)
	assert.Contains(t, module, "class_names")
	classNames := module["class_names"].([]interface{})
	assert.Greater(t, len(classNames), 0)
	assert.Contains(t, module, "train_pipeline")
	trainPipeline := module["train_pipeline"].([]interface{})
	assert.IsType(t, []interface{}{}, trainPipeline)
	assert.Contains(t, module, "test_pipeline")
	assert.Contains(t, module, "data")
	data := module["data"].(map[string]interface{})
	assert.IsType(t, map[string]interface{}{}, data)
	assert.Contains(t, module, "point_cloud_range")
	assert.Contains(t, module, "input_modality")
	_, trainOk := data["train"]
	_, valOk := data["val"]
	assert.True(t, trainOk)
	assert.True(t, valOk)
	_, testOk := data["test"]
	assert.True(t, testOk || valOk)
}

func TestPublicConfigsDataTwoFramesEdgeCases(t *testing.T) {
	path := "configs/mv2d/data/two_frames.py"
	module, err := tests.LoadPythonModule(path)
	assert.NoError(t, err)
	trainPipeline := module["train_pipeline"].([]interface{})
	for idx, stageRaw := range trainPipeline {
		stage, ok := stageRaw.(map[string]interface{})
		assert.Truef(t, ok, "train_pipeline[%d] must be dict", idx)
		val, ok := stage["type"]
		assert.Truef(t, ok, "'type' field required at train_pipeline[%d]", idx)
		_, ok = val.(string)
		assert.Truef(t, ok, "'type' value should be string at train_pipeline[%d]", idx)
		assert.NotEmptyf(t, val, "'type' is empty at train_pipeline[%d]", idx)
	}
}