package com.tusenai.mv2d.publictests;

import com.tusenai.mv2d.ConfigLoader;
import com.google.gson.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicConfigsExpPyTest {

    @Test
    public void testPublicConfigsExpPyImportable() throws Exception {
        String[] configPaths = {
            "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json",
            "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.json"
        };
        for (String configPath : configPaths) {
            JsonObject module = ConfigLoader.loadConfig(configPath);
            assertTrue(module.has("model"));
            assertTrue(module.get("model").isJsonObject());
            assertTrue(module.has("point_cloud_range"));
            assertTrue(module.has("roi_size"));
        }
    }

    @Test
    public void testPublicConfigsExpPyRoiStride() throws Exception {
        JsonObject module = ConfigLoader.loadConfig("configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.json");
        assertTrue(module.has("roi_srides"));
        JsonArray roiSrides = module.getAsJsonArray("roi_srides");
        assertEquals(1, roiSrides.size());
        assertEquals(16, roiSrides.get(0).getAsInt());
    }
}