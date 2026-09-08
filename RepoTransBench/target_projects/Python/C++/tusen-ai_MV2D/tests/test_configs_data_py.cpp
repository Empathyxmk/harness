#include <gtest/gtest.h>
#include "mv2d_config.h"

TEST(ConfigsDataPy, SingleFrameExecutable) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/single_frame.json", config));
    ASSERT_GT(config.class_names.size(), 0);
    ASSERT_GT(config.train_pipeline.size(), 0);
    ASSERT_GT(config.test_pipeline.size(), 0);
    ASSERT_GT(config.data.size(), 0);
    ASSERT_EQ(config.point_cloud_range.size(), 6);
    ASSERT_GT(config.input_modality.size(), 0);
    ASSERT_TRUE(config.data.count("train"));
    ASSERT_TRUE(config.data.count("val"));
    ASSERT_TRUE(config.data.count("test") || config.data.count("val"));
}

TEST(ConfigsDataPy, SingleFrameEdgeCases) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/single_frame.json", config));
    for (const auto& stage : config.train_pipeline) {
        ASSERT_TRUE(stage.count("type"));
        ASSERT_FALSE(stage.at("type").empty());
    }
}