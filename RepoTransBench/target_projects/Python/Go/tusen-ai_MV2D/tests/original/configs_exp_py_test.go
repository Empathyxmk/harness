package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tusanai/mv2d/tests"
)

var expConfigs = []string{
	"configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.py",
	"configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep72.py",
	"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
	"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py",
}

func TestConfigLoads(t *testing.T) {
	for _, configPath := range expConfigs {
		module, err := tests.LoadPythonModule(configPath)
		assert.NoError(t, err)
		assert.NotNil(t, module)
		assert.Contains(t, module, "model")
		assert.IsType(t, map[string]interface{}{}, module["model"])
		assert.Contains(t, module, "_base_")
		_ := module["_base_"]
		_, isList := _.([]interface{})
		_, isTuple := _.([]interface{})
		assert.True(t, isList || isTuple)
	}
}