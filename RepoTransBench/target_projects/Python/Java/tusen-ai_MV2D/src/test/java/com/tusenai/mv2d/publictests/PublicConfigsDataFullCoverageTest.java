package com.tusenai.mv2d.publictests;

import com.tusenai.mv2d.ConfigLoader;
import com.google.gson.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicConfigsDataFullCoverageTest {

    @Test
    public void testPublicDataConfigKeysAndTypes() throws Exception {
        JsonObject module = ConfigLoader.loadConfig("configs/mv2d/data/two_frames.json");
        assertTrue(module.has("class_names"));
        JsonArray classNames = module.getAsJsonArray("class_names");
        assertTrue(classNames.size() > 0);
        assertTrue(module.has("train_pipeline"));
        JsonArray trainPipeline = module.getAsJsonArray("train_pipeline");
        assertTrue(trainPipeline.size() > 0);
        for (JsonElement el : trainPipeline) {
            assertTrue(el.isJsonObject());
        }
        assertTrue(module.has("test_pipeline"));
        assertTrue(module.get("test_pipeline").isJsonArray());
        assertTrue(module.has("data"));
        JsonObject data = module.getAsJsonObject("data");
        assertTrue(data.has("train"));
        assertTrue(data.has("val"));
    }

    @Test
    public void testPublicPointCloudRangeVariety() throws Exception {
        JsonObject module = ConfigLoader.loadConfig("configs/mv2d/data/two_frames.json");
        assertTrue(module.has("point_cloud_range"));
        JsonArray pcr = module.getAsJsonArray("point_cloud_range");
        boolean hasNeg = false, hasPos = false;
        for (JsonElement el : pcr) {
            double v = el.getAsDouble();
            if (v < 0) hasNeg = true;
            if (v > 0) hasPos = true;
        }
        assertTrue(hasNeg && hasPos);
    }
}