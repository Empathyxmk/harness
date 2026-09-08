package com.tusenai.mv2d.publictests;

import com.tusenai.mv2d.ConfigLoader;
import com.google.gson.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicConfigsExpAttributesTest {

    private static final String[] PUBLIC_EXP_CONFIGS = {
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.json"
    };

    @Test
    public void testPublicModelConfigKeys() throws Exception {
        for (String configPath : PUBLIC_EXP_CONFIGS) {
            JsonObject module = ConfigLoader.loadConfig(configPath).getAsJsonObject("module");
            String[] requiredKeys = {"type", "use_grid_mask", "base_detector", "neck", "roi_head", "train_cfg"};
            for (String key : requiredKeys) {
                assertTrue(module.has(key), "Missing key: " + key + " in " + configPath);
            }
            JsonObject gm = module.getAsJsonObject("use_grid_mask");
            boolean anyTrueOrFloat = false;
            for (String field : gm.keySet()) {
                JsonElement val = gm.get(field);
                if (val.isJsonPrimitive()) {
                    if (val.getAsJsonPrimitive().isBoolean() && val.getAsBoolean())
                        anyTrueOrFloat = true;
                    if (val.getAsJsonPrimitive().isNumber())
                        anyTrueOrFloat = true;
                }
            }
            assertTrue(anyTrueOrFloat, "At least one grid mask option should be True or a float");
        }
    }

    @Test
    public void testPublicRoiHeadAndNested() throws Exception {
        String configPath = "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json";
        JsonObject module = ConfigLoader.loadConfig(configPath).getAsJsonObject("module");
        assertTrue(module.has("roi_head"));
        JsonObject rh = module.getAsJsonObject("roi_head");
        assertTrue(rh.has("bbox_roi_extractor"));
        assertTrue(rh.has("bbox_head"));
        assertTrue(rh.has("query_generator"));
        assertTrue(rh.has("pe"));

        if (rh.has("bbox_head")) {
            JsonObject bh = rh.getAsJsonObject("bbox_head");
            assertTrue(bh.has("transformer"));
            assertTrue(bh.has("bbox_coder"));
            int numClasses = bh.has("num_classes") ? bh.get("num_classes").getAsInt() : 1;
            assertTrue(numClasses > 0);
            if (bh.has("loss_cls")) {
                assertTrue(bh.get("loss_cls").isJsonObject());
            }
        }
        if (rh.has("pe")) {
            JsonObject pe = rh.getAsJsonObject("pe");
            assertTrue(pe.has("positional_encoding"));
        }
    }

    @Test
    public void testPublicTrainCfgDetections() throws Exception {
        for (String configPath : PUBLIC_EXP_CONFIGS) {
            JsonObject module = ConfigLoader.loadConfig(configPath).getAsJsonObject("module");
            if (module.has("train_cfg")) {
                JsonObject trainCfg = module.getAsJsonObject("train_cfg");
                if (trainCfg.has("detection_proposal")) {
                    JsonObject det = trainCfg.getAsJsonObject("detection_proposal");
                    assertTrue(det.has("score_thr"));
                    if (det.has("nms")) {
                        JsonObject nms = det.getAsJsonObject("nms");
                        assertTrue(nms.has("iou_threshold") || nms.has("class_agnostic"));
                    }
                }
            }
        }
    }

    @Test
    public void testPublicCodeWeightsVariations() throws Exception {
        String[] configPaths = {
            "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json",
            "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.json"
        };
        for (String configPath : configPaths) {
            JsonObject module = ConfigLoader.loadConfig(configPath).getAsJsonObject("module");
            JsonArray arr = module.getAsJsonObject("roi_head").getAsJsonObject("bbox_head")
                .getAsJsonArray("code_weights");
            assertTrue(arr.isJsonArray());
            assertEquals(10, arr.size());
            boolean allOnes = true;
            for (JsonElement e : arr) {
                assertTrue(e.isJsonPrimitive() && 
                    (e.getAsJsonPrimitive().isNumber() || e.getAsJsonPrimitive().isBoolean()));
                if (e.getAsDouble() != 1.0) allOnes = false;
            }
            assertFalse(allOnes, "code_weights should not all be 1.0 for public tests");
        }
    }

    @Test
    public void testPublicOperationOrderAndCp() throws Exception {
        for (String configPath : PUBLIC_EXP_CONFIGS) {
            JsonObject module = ConfigLoader.loadConfig(configPath).getAsJsonObject("module");
            JsonObject bboxHead = module.getAsJsonObject("roi_head").getAsJsonObject("bbox_head");
            if (!bboxHead.has("transformer")) continue;
            JsonObject tf = bboxHead.getAsJsonObject("transformer");
            if (!tf.has("decoder")) continue;
            JsonObject decoder = tf.getAsJsonObject("decoder");
            if (!decoder.has("transformerlayers")) continue;
            JsonObject tl = decoder.getAsJsonObject("transformerlayers");
            JsonElement oo = tl.get("operation_order");
            assertTrue(oo != null && (oo.isJsonArray()));
            JsonElement cp = tl.get("with_cp");
            assertTrue(cp.isJsonPrimitive() && (cp.getAsBoolean() == true || cp.getAsBoolean() == false));
        }
    }
}