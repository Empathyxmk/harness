package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tusanai/mv2d/tests"
)

var publicExpConfigs = []string{
	"configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.py",
	"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
	"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py",
}

func TestPublicModelConfigKeys(t *testing.T) {
	for _, configPath := range publicExpConfigs {
		module, err := tests.LoadPythonModule(configPath)
		assert.NoError(t, err)
		model := module["model"].(map[string]interface{})
		requiredKeys := []string{"type", "use_grid_mask", "base_detector", "neck", "roi_head", "train_cfg"}
		for _, k := range requiredKeys {
			_, ok := model[k]
			assert.Truef(t, ok, "Missing key: %s in %s", k, configPath)
		}
		gm := model["use_grid_mask"].(map[string]interface{})
		found := false
		for _, v := range gm {
			b, isBool := v.(bool)
			f, isFloat := v.(float64)
			if isBool && b {
				found = true
			}
			if isFloat {
				found = true
			}
		}
		assert.True(t, found, "At least one grid mask option should be True or a float")
	}
}

func TestPublicROIHeadAndNested(t *testing.T) {
	configPath := "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py"
	module, err := tests.LoadPythonModule(configPath)
	assert.NoError(t, err)
	model := module["model"].(map[string]interface{})
	rh := model["roi_head"].(map[string]interface{})
	_, ok := rh["bbox_roi_extractor"]
	assert.True(t, ok)
	_, ok = rh["bbox_head"]
	assert.True(t, ok)
	_, ok = rh["query_generator"]
	assert.True(t, ok)
	_, ok = rh["pe"]
	assert.True(t, ok)
	if bhRaw, ok := rh["bbox_head"]; ok {
		bh := bhRaw.(map[string]interface{})
		_, ok := bh["transformer"]
		assert.True(t, ok)
		_, ok = bh["bbox_coder"]
		assert.True(t, ok)
		numClasses, hasNum := bh["num_classes"]
		if hasNum {
			switch nc := numClasses.(type) {
			case int:
				assert.True(t, nc > 0)
			case float64:
				assert.True(t, nc > 0)
			}
		}
		if lossCls, ok := bh["loss_cls"]; ok {
			_, isDict := lossCls.(map[string]interface{})
			assert.True(t, isDict)
		}
	}
	if peRaw, ok := rh["pe"]; ok {
		pe := peRaw.(map[string]interface{})
		_, ok := pe["positional_encoding"]
		assert.True(t, ok)
	}
}

func TestPublicTrainCfgDetections(t *testing.T) {
	for _, configPath := range publicExpConfigs {
		module, err := tests.LoadPythonModule(configPath)
		assert.NoError(t, err)
		model := module["model"].(map[string]interface{})
		trainCfg := model["train_cfg"].(map[string]interface{})
		if detRaw, ok := trainCfg["detection_proposal"]; ok {
			det := detRaw.(map[string]interface{})
			_, ok := det["score_thr"]
			assert.True(t, ok)
			if nmsRaw, ok := det["nms"]; ok {
				nms := nmsRaw.(map[string]interface{})
				_, okIou := nms["iou_threshold"]
				_, okCls := nms["class_agnostic"]
				assert.True(t, okIou || okCls)
			}
		}
	}
}

func TestPublicCodeWeightsVariations(t *testing.T) {
	configPaths := []string{
		"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
		"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py",
	}
	for _, configPath := range configPaths {
		module, err := tests.LoadPythonModule(configPath)
		assert.NoError(t, err)
		bboxHead := module["model"].(map[string]interface{})["roi_head"].(map[string]interface{})["bbox_head"].(map[string]interface{})
		codeWeights := bboxHead["code_weights"].([]interface{})
		assert.Len(t, codeWeights, 10)
		allOne := true
		for _, w := range codeWeights {
			_, isNum := w.(float64)
			assert.True(t, isNum)
			if isNum && w.(float64) != 1.0 {
				allOne = false
			}
		}
		assert.False(t, allOne, "Not all code_weights should be exactly 1.0")
	}
}

func TestPublicOperationOrderAndCP(t *testing.T) {
	for _, configPath := range publicExpConfigs {
		module, err := tests.LoadPythonModule(configPath)
		assert.NoError(t, err)
		bboxHead := module["model"].(map[string]interface{})["roi_head"].(map[string]interface{})["bbox_head"].(map[string]interface{})
		decoderRaw, hasDecoder := bboxHead["transformer"].(map[string]interface{})["decoder"]
		if hasDecoder {
			decoder := decoderRaw.(map[string]interface{})
			tlayersRaw, ok := decoder["transformerlayers"]
			if ok {
				tlayers, _ := tlayersRaw.(map[string]interface{})
				oo, ok2 := tlayers["operation_order"]
				assert.True(t, ok2)
				switch oo.(type) {
				case []interface{}:
				default:
					assert.Fail(t, "operation_order must be list/tuple")
				}
				withCpSet, cpOk := tlayers["with_cp"]
				assert.True(t, cpOk)
				b, isBool := withCpSet.(bool)
				assert.True(t, isBool)
				assert.True(t, b || !b)
			}
		}
	}
}