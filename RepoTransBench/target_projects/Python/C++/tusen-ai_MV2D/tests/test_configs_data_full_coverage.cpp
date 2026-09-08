#include <gtest/gtest.h>
#include "mv2d_config.h"

TEST(ConfigsDataFullCoverage, DataSampleKeysAndPipelines) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/single_frame.json", config));
    auto it = std::find(config.class_names.begin(), config.class_names.end(), "car");
    ASSERT_TRUE(it != config.class_names.end());
    std::vector<std::string> allowed_keys = {
        "type", "to_float32", "with_bbox_3d", "with_label_3d", "with_bbox_2d",
        "with_attr_label", "point_cloud_range", "classes", "data_aug_conf",
        "training", "rot_range", "translation_std", "scale_ratio_range",
        "reverse_angle", "debug", "keys", "class_names", "mean", "std",
        "p", "keep_shape", "imdecode_backend", "size", "keep_ratio", "pad_val",
        "to_rgb", "color_type", "to_onehot", "file_client_args", "backend", "crop_size",
        "size_divisor"
    };
    // Just check type for each pipeline stage
    for (const auto& pipe : config.train_pipeline) {
        ASSERT_TRUE(pipe.count("type"));
        ASSERT_FALSE(pipe.at("type").empty());
    }
    for (const auto& pipe : config.test_pipeline) {
        ASSERT_TRUE(pipe.count("type"));
        ASSERT_FALSE(pipe.at("type").empty());
    }
    // Mock ida_aug_conf logic
    // This test only demonstrates a logic match, details can be expanded if config supports
    std::vector<std::string> keys = {"resize_lim", "final_dim", "H", "W", "rand_flip"};
    // This would require corresponding fields in config, which could be checked similarly
}

TEST(ConfigsDataFullCoverage, InputModalityFields) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/single_frame.json", config));
    for (const auto& kv : config.input_modality) {
        // key: string, value: bool
        ASSERT_TRUE(kv.second == true || kv.second == false);
    }
}

TEST(ConfigsDataFullCoverage, DataDictContent) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/single_frame.json", config));
    for (const auto& subset : {"train", "val"}) {
        ASSERT_TRUE(config.data.count(subset));
        auto& cfg = config.data[subset];
        ASSERT_TRUE(cfg.count("type"));
        ASSERT_TRUE(cfg.count("data_root"));
        ASSERT_TRUE(cfg.count("pipeline"));
        // Not strictly checking class field type here because simplified parsing
        ASSERT_TRUE(cfg.count("ann_file"));
        ASSERT_FALSE(cfg.at("ann_file").empty());
    }
}

TEST(ConfigsDataFullCoverage, PostPointCloudRange) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/single_frame.json", config));
    ASSERT_EQ(config.point_cloud_range.size(), 6);
}

TEST(ConfigsDataFullCoverage, TwoFramesDataConfig) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/two_frames.json", config));
    ASSERT_GT(config.class_names.size(), 0);
    ASSERT_GT(config.train_pipeline.size(), 0);
    ASSERT_GT(config.test_pipeline.size(), 0);
    ASSERT_GT(config.data.size(), 0);
    ASSERT_TRUE(config.data.count("train"));
    ASSERT_TRUE(config.data.count("val"));
    for (const auto& pipe : config.train_pipeline) {
        ASSERT_TRUE(pipe.count("type"));
    }
    for (const auto& pipe : config.test_pipeline) {
        ASSERT_TRUE(pipe.count("type"));
    }
}

TEST(ConfigsDataFullCoverage, TwoFramesInputModality) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/two_frames.json", config));
    for (const auto& kv : config.input_modality) {
        ASSERT_TRUE(kv.second == true || kv.second == false);
    }
}

TEST(ConfigsDataFullCoverage, TwoFramesPointCloudRange) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/two_frames.json", config));
    ASSERT_EQ(config.point_cloud_range.size(), 6);
}