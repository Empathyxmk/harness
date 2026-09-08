package original

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tusanai/mv2d/tests"
)

func TestDataSampleKeysAndPipelines(t *testing.T) {
	mod, err := tests.LoadPythonModule("configs/mv2d/data/single_frame.py")
	assert.NoError(t, err)
	classNames := mod["class_names"].([]interface{})
	foundCar := false
	for _, v := range classNames {
		if v.(string) == "car" {
			foundCar = true
		}
	}
	assert.True(t, foundCar)

	allowedKeys := map[string]bool{
		"type": true, "to_float32": true, "with_bbox_3d": true, "with_label_3d": true, "with_bbox_2d": true,
		"with_attr_label": true, "point_cloud_range": true, "classes": true, "data_aug_conf": true,
		"training": true, "rot_range": true, "translation_std": true, "scale_ratio_range": true,
		"reverse_angle": true, "debug": true, "keys": true, "class_names": true, "mean": true, "std": true,
		"p": true, "keep_shape": true, "imdecode_backend": true, "size": true, "keep_ratio": true,
		"pad_val": true, "to_rgb": true, "color_type": true, "to_onehot": true, "file_client_args": true,
		"backend": true, "crop_size": true, "size_divisor": true,
	}
	fullPipeline := append(mod["train_pipeline"].([]interface{}), mod["test_pipeline"].([]interface{})...)

	for _, pipeRaw := range fullPipeline {
		pipe := pipeRaw.(map[string]interface{})
		_, ok := pipe["type"].(string)
		assert.True(t, ok)
	}
	idaAugConf := mod["ida_aug_conf"].(map[string]interface{})
	for _, k := range []string{"resize_lim", "final_dim", "H", "W", "rand_flip"} {
		assert.Contains(t, idaAugConf, k)
	}
	for _, stageRaw := range mod["train_pipeline"].([]interface{}) {
		stage := stageRaw.(map[string]interface{})
		for key := range stage {
			assert.Truef(t, allowedKeys[key], "Unexpected key '%s' in pipeline stage: %+v", key, stage)
		}
	}
}

func TestInputModalityFields(t *testing.T) {
	mod, err := tests.LoadPythonModule("configs/mv2d/data/single_frame.py")
	assert.NoError(t, err)
	inputMod := mod["input_modality"].(map[string]interface{})
	for _, v := range inputMod {
		_, ok := v.(bool)
		assert.True(t, ok)
	}
}

func TestDataDictContent(t *testing.T) {
	mod, err := tests.LoadPythonModule("configs/mv2d/data/single_frame.py")
	assert.NoError(t, err)
	for _, subset := range []string{"train", "val"} {
		assert.Contains(t, mod["data"], subset)
		cfg := mod["data"].(map[string]interface{})[subset].(map[string]interface{})
		assert.Contains(t, cfg, "type")
		assert.Contains(t, cfg, "data_root")
		assert.Contains(t, cfg, "pipeline")
		assert.IsType(t, []interface{}{}, cfg["classes"])
		assert.Contains(t, cfg, "ann_file")
		assert.IsType(t, "", cfg["ann_file"])
		if af2d, ok := cfg["ann_file_2d"]; ok {
			str := af2d.(string)
			assert.IsType(t, "", str)
			assert.True(t, strings.HasSuffix(str, ".json"))
		}
		if tm, ok := cfg["test_mode"]; ok {
			b, isBool := tm.(bool)
			assert.True(t, isBool)
			assert.True(t, b == true || b == false)
		}
	}
}

func TestPostPointCloudRange(t *testing.T) {
	mod, err := tests.LoadPythonModule("configs/mv2d/data/single_frame.py")
	assert.NoError(t, err)
	pcRange := mod["point_cloud_range"].([]interface{})
	assert.Len(t, pcRange, 6)
}

func TestTwoFramesDataConfig(t *testing.T) {
	mod, err := tests.LoadPythonModule("configs/mv2d/data/two_frames.py")
	assert.NoError(t, err)
	_, ok := mod["class_names"].([]interface{})
	assert.True(t, ok)
	assert.IsType(t, []interface{}{}, mod["train_pipeline"])
	assert.IsType(t, []interface{}{}, mod["test_pipeline"])
	data := mod["data"].(map[string]interface{})
	_, trainOk := data["train"]
	_, valOk := data["val"]
	assert.True(t, trainOk && valOk)
	fullPipeline := append(mod["train_pipeline"].([]interface{}), mod["test_pipeline"].([]interface{})...)
	for _, pipeRaw := range fullPipeline {
		pipe := pipeRaw.(map[string]interface{})
		_, ok := pipe["type"]
		assert.True(t, ok)
	}
}

func TestTwoFramesInputModality(t *testing.T) {
	mod, err := tests.LoadPythonModule("configs/mv2d/data/two_frames.py")
	assert.NoError(t, err)
	inputMod := mod["input_modality"].(map[string]interface{})
	for _, v := range inputMod {
		_, ok := v.(bool)
		assert.True(t, ok)
	}
}

func TestTwoFramesPointCloudRange(t *testing.T) {
	mod, err := tests.LoadPythonModule("configs/mv2d/data/two_frames.py")
	assert.NoError(t, err)
	pcRange := mod["point_cloud_range"].([]interface{})
	assert.Len(t, pcRange, 6)
}