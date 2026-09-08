package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tusanai/mv2d/tests"
)

func TestPublicConfigsExpPyImportable(t *testing.T) {
	configPaths := []string{
		"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
		"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py",
	}
	for _, path := range configPaths {
		module, err := tests.LoadPythonModule(path)
		assert.NoError(t, err)
		assert.NotNil(t, module)
		assert.Contains(t, module, "model")
		assert.IsType(t, map[string]interface{}{}, module["model"])
		assert.Contains(t, module, "point_cloud_range")
		assert.Contains(t, module, "roi_size")
	}
}

func TestPublicConfigsExpPyROIStride(t *testing.T) {
	path := "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py"
	module, err := tests.LoadPythonModule(path)
	assert.NoError(t, err)
	assert.NotNil(t, module)
	assert.Contains(t, module, "roi_srides")
	val := module["roi_srides"].([]interface{})
	assert.Len(t, val, 1)
	if len(val) > 0 {
		assert.Equal(t, 16, int(val[0].(float64)))
	}
}