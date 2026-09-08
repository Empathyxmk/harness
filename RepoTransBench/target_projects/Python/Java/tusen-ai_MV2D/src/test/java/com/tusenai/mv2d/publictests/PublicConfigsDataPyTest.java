package com.tusenai.mv2d.publictests;

import com.tusenai.mv2d.ConfigLoader;
import com.google.gson.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicConfigsDataPyTest {

    @Test
    public void testPublicConfigsDataTwoFramesExecutable() throws Exception {
        JsonObject module = ConfigLoader.loadConfig("configs/mv2d/data/two_frames.json");
        assertTrue(module.has("class_names"));
        JsonArray classNames = module.getAsJsonArray("class_names");
        assertTrue(classNames.size() > 0);
        assertTrue(module.has("train_pipeline"));
        assertTrue(module.get("train_pipeline").isJsonArray());
        assertTrue(module.has("test_pipeline"));
        assertTrue(module.has("data"));
        assertTrue(module.get("data").isJsonObject());
        assertTrue(module.has("point_cloud_range"));
        assertTrue(module.has("input_modality"));
        JsonObject data = module.getAsJsonObject("data");
        assertTrue(data.has("train"));
        assertTrue(data.has("val"));
        assertTrue(data.has("test") || data.has("val"));
    }

    @Test
    public void testPublicConfigsDataTwoFramesEdgeCases() throws Exception {
        JsonObject module = ConfigLoader.loadConfig("configs/mv2d/data/two_frames.json");
        JsonArray trainPipeline = module.getAsJsonArray("train_pipeline");
        for (JsonElement el : trainPipeline) {
            assertTrue(el.isJsonObject());
            JsonObject stage = el.getAsJsonObject();
            assertTrue(stage.has("type"));
            assertTrue(stage.get("type").isJsonPrimitive());
            assertFalse(stage.get("type").getAsString().isEmpty());
        }
    }
}