package com.tusenai.mv2d.original;

import com.tusenai.mv2d.ConfigLoader;
import com.google.gson.*;
import org.junit.jupiter.api.*;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class ConfigsExpPyTest {

    private static final String[] EXP_CONFIGS = {
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep72.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.json"
    };

    @Test
    public void testConfigLoads() throws Exception {
        for(String configPath : EXP_CONFIGS) {
            JsonObject module = ConfigLoader.loadConfig(configPath);
            // Check basic expected attributes
            assertTrue(module.has("model"));
            assertTrue(module.get("model").isJsonObject());
            assertTrue(module.has("_base_"));
            JsonElement baseObj = module.get("_base_");
            assertTrue(baseObj.isJsonArray() || baseObj.isJsonObject());
        }
    }
}