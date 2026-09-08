#include <gtest/gtest.h>
#include "mv2d_config.h"

TEST(PublicConfigsDataFullCoverage, DataConfigKeysAndTypes) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/two_frames.json", config));
    ASSERT_GT(config.class_names.size(), 0);
    ASSERT_GT(config.train_pipeline.size(), 0);
    ASSERT_TRUE(std::all_of(config.train_pipeline.begin(), config.train_pipeline.end(),
        [](const std::map<std::string, std::string>& stg) { return stg.count("type"); }));
    ASSERT_GT(config.test_pipeline.size(), 0);
    ASSERT_GT(config.data.size(), 0);
    ASSERT_TRUE(config.data.count("train"));
    ASSERT_TRUE(config.data.count("val"));
}

TEST(PublicConfigsDataFullCoverage, PointCloudRangeVariety) {
    MV2DConfig config;
    ASSERT_TRUE(load_mv2d_config("configs/mv2d/data/two_frames.json", config));
    ASSERT_EQ(config.point_cloud_range.size(), 6);
    bool has_neg = false, has_pos = false;
    for (float x : config.point_cloud_range) {
        if (x < 0) has_neg = true;
        if (x > 0) has_pos = true;
    }
    ASSERT_TRUE(has_neg && has_pos);
}