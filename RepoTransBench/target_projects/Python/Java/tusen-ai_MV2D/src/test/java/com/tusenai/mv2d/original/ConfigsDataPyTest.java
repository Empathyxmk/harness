package com.tusenai.mv2d.original;

import com.tusenai.mv2d.ConfigLoader;
import com.google.gson.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class ConfigsDataPyTest {

    @Test
    public void testConfigsDataSingleFrameExecutable() throws Exception {
        JsonObject module = ConfigLoader.loadConfig("configs/mv2d/data/single_frame.json");
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
    public void testConfigsDataSingleFrameEdgeCases() throws Exception {
        JsonObject module = ConfigLoader.loadConfig("configs/mv2d/data/single_frame.json");
        JsonArray trainPipeline = module.getAsJsonArray("train_pipeline");
        for (JsonElement el : trainPipeline) {
            assertTrue(el.isJsonObject());
            JsonObject stage = el.getAsJsonObject();
            assertTrue(stage.has("type"));
            assertTrue(stage.get("type").isJsonPrimitive());
            assertTrue(!stage.get("type").getAsString().isEmpty());
        }
    }
}