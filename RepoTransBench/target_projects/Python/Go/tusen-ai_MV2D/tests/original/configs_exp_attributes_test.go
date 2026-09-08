package original

import (
	"os"
	"path/filepath"
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

// Helper: Loads a python config as a generic map
func loadConfigModule(path string) (map[string]interface{}, error) {
	return tests.LoadPythonModule(path)
}

func TestModelConfigKeys(t *testing.T) {
	for _, configPath := range expConfigs {
		module, err := loadConfigModule(configPath)
		assert.NoError(t, err)
		model := module["model"].(map[string]interface{})
		requiredKeys := []string{"type", "use_grid_mask", "base_detector", "neck", "roi_head", "train_cfg"}
		for _, key := range requiredKeys {
			_, ok := model[key]
			assert.Truef(t, ok, "Missing key: %s in %s", key, configPath)
		}
		gm := model["use_grid_mask"].(map[string]interface{})
		found := false
		for _, v := range gm {
			switch v := v.(type) {
			case bool:
				if v {
					found = true
				}
			case float64, int:
				if v != 0 {
					found = true
				}
			}
		}
		assert.True(t, found, "At least one grid mask option should be True or >0")
	}
}

func TestROIHeadAndNested(t *testing.T) {
	configPath := "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.py"
	module, err := loadConfigModule(configPath)
	assert.NoError(t, err)
	model := module["model"].(map[string]interface{})
	rh, ok := model["roi_head"].(map[string]interface{})
	assert.True(t, ok)
	_, ok = rh["bbox_roi_extractor"]
	assert.True(t, ok)
	_, ok = rh["bbox_head"]
	assert.True(t, ok)
	_, ok = rh["query_generator"]
	assert.True(t, ok)
	_, ok = rh["pe"]
	assert.True(t, ok)

	if bhRaw, ok := rh["bbox_head"]; ok {
		bh, _ := bhRaw.(map[string]interface{})
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
			default:
				assert.Fail(t, "num_classes is not int/float", nc)
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

func TestTrainCfgDetections(t *testing.T) {
	for _, configPath := range expConfigs {
		module, err := loadConfigModule(configPath)
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

func TestCodeWeightsVariations(t *testing.T) {
	configPaths := []string{
		"configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.py",
		"configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
	}
	for _, configPath := range configPaths {
		module, err := loadConfigModule(configPath)
		assert.NoError(t, err)
		bboxHead := module["model"].(map[string]interface{})["roi_head"].(map[string]interface{})["bbox_head"].(map[string]interface{})
		codeWeights := bboxHead["code_weights"].([]interface{})
		assert.Len(t, codeWeights, 10)
		for _, w := range codeWeights {
			switch w.(type) {
			case float64, int:
				// ok
			default:
				assert.Fail(t, "code_weights must only contain float64/int")
			}
		}
	}
}

func TestOperationOrderAndCP(t *testing.T) {
	for _, configPath := range expConfigs {
		module, err := loadConfigModule(configPath)
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
					// ok
				default:
					assert.Fail(t, "operation_order must be list or tuple")
				}
				withCpSet, cpOk := tlayers["with_cp"]
				assert.True(t, cpOk)
				if b, ok := withCpSet.(bool); ok {
					assert.True(t, b == true || b == false)
				}
			}
		}
	}
}