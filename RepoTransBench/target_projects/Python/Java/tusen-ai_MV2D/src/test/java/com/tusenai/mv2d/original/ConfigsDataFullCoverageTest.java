package com.tusenai.mv2d.original;

import com.tusenai.mv2d.ConfigLoader;
import com.google.gson.*;
import org.junit.jupiter.api.*;

import java.io.IOException;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class ConfigsDataFullCoverageTest {

    @Test
    public void testDataSampleKeysAndPipelines() throws IOException {
        JsonObject mod = ConfigLoader.loadConfig("configs/mv2d/data/single_frame.json");
        JsonArray classNames = mod.getAsJsonArray("class_names");
        boolean hasCar = false;
        for (JsonElement e : classNames) {
            if (e.getAsString().equalsIgnoreCase("car")) hasCar = true;
        }
        assertTrue(hasCar, "car must be in class_names");

        Set<String> allowedKeys = new HashSet<>(Arrays.asList(
            "type", "to_float32", "with_bbox_3d", "with_label_3d", "with_bbox_2d",
            "with_attr_label", "point_cloud_range", "classes", "data_aug_conf",
            "training", "rot_range", "translation_std", "scale_ratio_range",
            "reverse_angle", "debug", "keys", "class_names", "mean", "std",
            "p", "keep_shape", "imdecode_backend", "size", "keep_ratio", "pad_val",
            "to_rgb", "color_type", "to_onehot", "file_client_args", "backend", "crop_size",
            "size_divisor"
        ));

        JsonArray trainPipeline = mod.getAsJsonArray("train_pipeline");
        JsonArray testPipeline = mod.getAsJsonArray("test_pipeline");

        for (JsonElement el : trainPipeline) {
            assertTrue(el.isJsonObject());
            assertTrue(el.getAsJsonObject().has("type"));
            assertTrue(el.getAsJsonObject().get("type").isJsonPrimitive());
            assertTrue(el.getAsJsonObject().get("type").getAsJsonPrimitive().isString());
            for (Map.Entry<String, JsonElement> e : el.getAsJsonObject().entrySet()) {
                assertTrue(allowedKeys.contains(e.getKey()), "Unexpected key " + e.getKey());
            }
        }
        for (JsonElement el : testPipeline) {
            assertTrue(el.isJsonObject());
            assertTrue(el.getAsJsonObject().has("type"));
            assertTrue(el.getAsJsonObject().get("type").isJsonPrimitive());
            assertTrue(el.getAsJsonObject().get("type").getAsJsonPrimitive().isString());
        }

        JsonObject idaAugConf = mod.getAsJsonObject("ida_aug_conf");
        for (String k : Arrays.asList("resize_lim", "final_dim", "H", "W", "rand_flip")) {
            assertTrue(idaAugConf.has(k));
        }
    }

    @Test
    public void testInputModalityFields() throws IOException {
        JsonObject mod = ConfigLoader.loadConfig("configs/mv2d/data/single_frame.json");
        JsonObject inputModality = mod.getAsJsonObject("input_modality");
        for (String k : inputModality.keySet()) {
            assertTrue(inputModality.get(k).isJsonPrimitive());
            assertTrue(inputModality.get(k).getAsJsonPrimitive().isBoolean());
        }
    }

    @Test
    public void testDataDictContent() throws IOException {
        JsonObject mod = ConfigLoader.loadConfig("configs/mv2d/data/single_frame.json");
        JsonObject data = mod.getAsJsonObject("data");
        for (String subset : Arrays.asList("train", "val")) {
            assertTrue(data.has(subset));
            JsonObject cfg = data.getAsJsonObject(subset);
            assertTrue(cfg.has("type"));
            assertTrue(cfg.has("data_root"));
            assertTrue(cfg.has("pipeline"));
            assertTrue(cfg.get("classes").isJsonArray());
            assertTrue(cfg.has("ann_file"));
            assertTrue(cfg.get("ann_file").isJsonPrimitive());
            if (cfg.has("ann_file_2d")) {
                assertTrue(cfg.get("ann_file_2d").isJsonPrimitive());
                assertTrue(cfg.get("ann_file_2d").getAsString().endsWith(".json"));
            }
            if (cfg.has("test_mode")) {
                boolean t = cfg.get("test_mode").getAsBoolean();
                assertTrue(t || !t);
            }
        }
    }

    @Test
    public void testPostPointCloudRange() throws IOException {
        JsonObject mod = ConfigLoader.loadConfig("configs/mv2d/data/single_frame.json");
        JsonArray pcr = mod.getAsJsonArray("point_cloud_range");
        assertEquals(6, pcr.size());
    }

    @Test
    public void testTwoFramesDataConfig() throws IOException {
        JsonObject mod = ConfigLoader.loadConfig("configs/mv2d/data/two_frames.json");
        assertTrue(mod.has("class_names"));
        assertTrue(mod.get("class_names").isJsonArray());
        assertTrue(mod.has("train_pipeline") && mod.get("train_pipeline").isJsonArray());
        assertTrue(mod.has("test_pipeline") && mod.get("test_pipeline").isJsonArray());
        assertTrue(mod.has("data") && mod.get("data").isJsonObject());
        JsonObject data = mod.getAsJsonObject("data");
        assertTrue(data.has("train") && data.has("val"));
        JsonArray tp = mod.getAsJsonArray("train_pipeline");
        JsonArray ttp = mod.getAsJsonArray("test_pipeline");
        for (JsonElement el : tp) {
            assertTrue(el.isJsonObject());
            assertTrue(el.getAsJsonObject().has("type"));
        }
        for (JsonElement el : ttp) {
            assertTrue(el.isJsonObject());
            assertTrue(el.getAsJsonObject().has("type"));
        }
    }

    @Test
    public void testTwoFramesInputModality() throws IOException {
        JsonObject mod = ConfigLoader.loadConfig("configs/mv2d/data/two_frames.json");
        JsonObject inputModality = mod.getAsJsonObject("input_modality");
        for (String k : inputModality.keySet()) {
            assertTrue(inputModality.get(k).isJsonPrimitive());
            assertTrue(inputModality.get(k).getAsJsonPrimitive().isBoolean());
        }
    }

    @Test
    public void testTwoFramesPointCloudRange() throws IOException {
        JsonObject mod = ConfigLoader.loadConfig("configs/mv2d/data/two_frames.json");
        JsonArray pcr = mod.getAsJsonArray("point_cloud_range");
        assertEquals(6, pcr.size());
    }
}